# Web-Socket Learning

## What is web-socket?

WebSocket is a full-duplex communication protocol that allows for persistent, bidirectional communication between client and server over a single **TCP connection**.

### Comparison with HTTP

* HTTP: Request-response model (client initiates).

* WebSocket: Continuous connection (either side can send messages anytime).

## How TCP Underpins WebSockets

* **Transport Layer Foundation:** TCP is a transport layer protocol that provides reliable, ordered, and error-checked delivery of data between applications. WebSocket is a higher-level protocol that operates on top of TCP, using its reliable connection as the basis for its own communication model.

* **Connection Establishment:** A WebSocket connection begins with an HTTP handshake that uses the HTTP Upgrade header to switch from HTTP to the WebSocket protocol. Once established, the connection persists as a single TCP connection, enabling ongoing, full-duplex (two-way) communication between client and server.

* **Message Framing:** While TCP transmits a continuous stream of bytes, WebSockets introduce their own framing mechanism. Data sent over a WebSocket is organized into discrete messages, each with its own frame header, allowing the application to work with complete messages rather than arbitrary byte streams.

* **Reliability and Ordering:** All WebSocket messages benefit from TCP’s guarantees of reliable and in-order delivery. This is essential for real-time web applications—such as live chat, gaming, and collaborative editing—where message loss or disorder would degrade the user experience.

## Why WebSockets Use TCP

* **Full-Duplex Communication:** WebSockets enable both client and server to send data independently and simultaneously over a single TCP connection, unlike HTTP’s request-response model.

* **Low Overhead:** After the initial handshake, the protocol overhead is minimal, making WebSockets efficient for high-frequency, real-time data exchange.

* **Firewall and Proxy Compatibility:** By leveraging standard HTTP ports (80 and 443) for the handshake, WebSockets can traverse most firewalls and proxies that would otherwise block custom protocols.

