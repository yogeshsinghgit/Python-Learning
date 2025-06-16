from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import asyncio
from datetime import datetime
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="WebSocket Notification System", version="1.0.0")

# Pydantic models for request/response
class NotificationRequest(BaseModel):
    user_id: Optional[str] = None
    message: str
    notification_type: str = "info"  # info, success, warning, error
    title: Optional[str] = None

class NotificationResponse(BaseModel):
    id: str
    user_id: Optional[str]
    message: str
    notification_type: str
    title: Optional[str]
    timestamp: str

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        # Store active connections: {user_id: [websocket_connections]}
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # Store connection metadata
        self.connection_info: Dict[WebSocket, Dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept and store a new WebSocket connection"""
        await websocket.accept()
        
        # Initialize user connections list if not exists
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        # Add connection to user's list
        self.active_connections[user_id].append(websocket)
        
        # Store connection metadata
        self.connection_info[websocket] = {
            "user_id": user_id,
            "connected_at": datetime.now().isoformat(),
            "connection_id": str(uuid.uuid4())
        }
        
        logger.info(f"User {user_id} connected. Total connections: {len(self.active_connections[user_id])}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        if websocket in self.connection_info:
            user_id = self.connection_info[websocket]["user_id"]
            
            # Remove from active connections
            if user_id in self.active_connections:
                self.active_connections[user_id].remove(websocket)
                
                # Clean up empty user entry
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
            
            # Remove connection info
            del self.connection_info[websocket]
            
            logger.info(f"User {user_id} disconnected")
    
    async def send_personal_message(self, message: str, user_id: str):
        """Send a message to a specific user's all connections"""
        if user_id in self.active_connections:
            disconnected_connections = []
            
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending message to {user_id}: {e}")
                    disconnected_connections.append(connection)
            
            # Clean up disconnected connections
            for conn in disconnected_connections:
                self.disconnect(conn)
    
    async def broadcast(self, message: str):
        """Send a message to all connected users"""
        disconnected_connections = []
        
        for user_id, connections in self.active_connections.items():
            for connection in connections:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to {user_id}: {e}")
                    disconnected_connections.append(connection)
        
        # Clean up disconnected connections
        for conn in disconnected_connections:
            self.disconnect(conn)
    
    def get_active_users(self) -> List[str]:
        """Get list of currently connected users"""
        return list(self.active_connections.keys())
    
    def get_connection_count(self) -> int:
        """Get total number of active connections"""
        return sum(len(connections) for connections in self.active_connections.values())

# Initialize connection manager
manager = ConnectionManager()

# WebSocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time notifications"""
    await manager.connect(websocket, user_id)
    
    try:
        # Send welcome message
        welcome_notification = NotificationResponse(
            id=str(uuid.uuid4()),
            user_id=user_id,
            message=f"Welcome {user_id}! You are now connected to the notification system.",
            notification_type="success",
            title="Connected",
            timestamp=datetime.now().isoformat()
        )
        await websocket.send_text(welcome_notification.json())
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Wait for messages from client (optional heartbeat/ping)
                data = await websocket.receive_text()
                
                # Handle client messages (ping/pong for connection health)
                if data == "ping":
                    await websocket.send_text("pong")
                else:
                    # Echo back client message with timestamp
                    echo_notification = NotificationResponse(
                        id=str(uuid.uuid4()),
                        user_id=user_id,
                        message=f"Echo: {data}",
                        notification_type="info",
                        title="Echo",
                        timestamp=datetime.now().isoformat()
                    )
                    await websocket.send_text(echo_notification.json())
                    
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error in websocket loop for {user_id}: {e}")
                break
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for user: {user_id}")
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
    finally:
        manager.disconnect(websocket)

# REST API endpoints
@app.post("/send-notification", response_model=NotificationResponse)
async def send_notification(notification: NotificationRequest):
    """Send a notification to a specific user or broadcast to all users"""
    
    # Create notification response object
    notification_response = NotificationResponse(
        id=str(uuid.uuid4()),
        user_id=notification.user_id,
        message=notification.message,
        notification_type=notification.notification_type,
        title=notification.title or "Notification",
        timestamp=datetime.now().isoformat()
    )
    
    try:
        if notification.user_id:
            # Send to specific user
            if notification.user_id in manager.active_connections:
                await manager.send_personal_message(
                    notification_response.json(), 
                    notification.user_id
                )
                logger.info(f"Notification sent to user: {notification.user_id}")
            else:
                raise HTTPException(
                    status_code=404, 
                    detail=f"User {notification.user_id} is not connected"
                )
        else:
            # Broadcast to all users
            await manager.broadcast(notification_response.json())
            logger.info("Notification broadcasted to all users")
        
        return notification_response
        
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        raise HTTPException(status_code=500, detail="Failed to send notification")

@app.get("/active-users")
async def get_active_users():
    """Get list of currently connected users"""
    return {
        "active_users": manager.get_active_users(),
        "total_connections": manager.get_connection_count(),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_connections": manager.get_connection_count(),
        "timestamp": datetime.now().isoformat()
    }

# Serve static HTML client for testing
@app.get("/")
async def get_client():
    """Serve a simple HTML client for testing WebSocket connections"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebSocket Notification Client</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 800px; margin: 0 auto; }
            .notification { 
                padding: 10px; margin: 5px 0; border-radius: 5px; 
                border-left: 4px solid #007bff;
            }
            .notification.success { border-left-color: #28a745; background-color: #d4edda; }
            .notification.error { border-left-color: #dc3545; background-color: #f8d7da; }
            .notification.warning { border-left-color: #ffc107; background-color: #fff3cd; }
            .notification.info { border-left-color: #17a2b8; background-color: #d1ecf1; }
            input, button { padding: 8px; margin: 5px; }
            button { background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background-color: #0056b3; }
            #messages { height: 300px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>WebSocket Notification System</h1>
            
            <div>
                <input type="text" id="userId" placeholder="Enter User ID" value="user123">
                <button onclick="connect()">Connect</button>
                <button onclick="disconnect()">Disconnect</button>
                <span id="status">Disconnected</span>
            </div>
            
            <div>
                <input type="text" id="messageInput" placeholder="Enter message to send">
                <button onclick="sendMessage()">Send Message</button>
            </div>
            
            <div>
                <h3>Notifications:</h3>
                <div id="messages"></div>
            </div>
        </div>

        <script>
            let ws = null;
            let userId = null;

            function connect() {
                userId = document.getElementById('userId').value;
                if (!userId) {
                    alert('Please enter a User ID');
                    return;
                }

                ws = new WebSocket(`ws://localhost:8000/ws/${userId}`);
                
                ws.onopen = function(event) {
                    document.getElementById('status').textContent = 'Connected';
                    document.getElementById('status').style.color = 'green';
                };

                ws.onmessage = function(event) {
                    const notification = JSON.parse(event.data);
                    displayNotification(notification);
                };

                ws.onclose = function(event) {
                    document.getElementById('status').textContent = 'Disconnected';
                    document.getElementById('status').style.color = 'red';
                };

                ws.onerror = function(error) {
                    console.error('WebSocket error:', error);
                };
            }

            function disconnect() {
                if (ws) {
                    ws.close();
                }
            }

            function sendMessage() {
                const message = document.getElementById('messageInput').value;
                if (ws && message) {
                    ws.send(message);
                    document.getElementById('messageInput').value = '';
                }
            }

            function displayNotification(notification) {
                const messagesDiv = document.getElementById('messages');
                const notificationDiv = document.createElement('div');
                notificationDiv.className = `notification ${notification.notification_type}`;
                
                notificationDiv.innerHTML = `
                    <strong>${notification.title}</strong><br>
                    ${notification.message}<br>
                    <small>Time: ${new Date(notification.timestamp).toLocaleString()}</small>
                `;
                
                messagesDiv.appendChild(notificationDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }

            // Auto-connect with default user for demo
            window.onload = function() {
                setTimeout(connect, 1000);
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Background task example - Send periodic notifications
@app.on_event("startup")
async def startup_event():
    """Background task to send periodic notifications"""
    asyncio.create_task(periodic_notifications())

async def periodic_notifications():
    """Send periodic notifications to all connected users"""
    while True:
        await asyncio.sleep(30)  # Wait 30 seconds
        
        if manager.get_connection_count() > 0:
            periodic_notification = NotificationResponse(
                id=str(uuid.uuid4()),
                user_id=None,
                message="This is a periodic system notification sent every 30 seconds.",
                notification_type="info",
                title="System Update",
                timestamp=datetime.now().isoformat()
            )
            
            await manager.broadcast(periodic_notification.json())
            logger.info("Periodic notification sent to all users")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)