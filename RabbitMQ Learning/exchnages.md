# 🔄 **RabbitMQ Exchange Types (4 Types)**

Exchanges decide *how messages are routed to queues*.
RabbitMQ has **4 exchange types**:

1. **Direct Exchange**
2. **Fanout Exchange**
3. **Topic Exchange**
4. **Headers Exchange**

Let’s understand them one by one.

---

# 1️⃣ **Direct Exchange**

### **Routing based on exact matching of the routing key.**

📌 **Rule:** Queue receives a message **only if routing key == binding key**

### **Diagram (in words):**

```
Producer → Exchange (direct) → Queue (if routing key matches binding key)
```

### **Example:**

You have services for:

* `email`
* `sms`
* `push`

Bindings:

* Queue A: binding key = `email`
* Queue B: binding key = `sms`

If producer sends:

* Message with routing key = `email` → Goes to Queue A
* Message with routing key = `sms` → Goes to Queue B
* routing key = `push` → No match → Goes nowhere

### **Where used:**

✔ Notification systems
✔ Microservices with specific event handlers
✔ Clean one-to-one routing

---

# 2️⃣ **Fanout Exchange**

### **Sends the message to ALL queues bound to it.**

📌 **Rule:** Ignores the routing key completely. Broadcast.

### **Diagram:**

```
Producer → Fanout Exchange → Queue A
                               Queue B
                               Queue C    (ALL get the message)
```

### **Example:**

An event: **"UserSignedUp"**

Queues bound:

* Send welcome email
* Add to CRM
* Log analytics
* Send coupon

All get the same message.

### **Where used:**

✔ Broadcast systems
✔ Notifications to multiple services
✔ Cache invalidation
✔ Real-time events

---

# 3️⃣ **Topic Exchange**

### **Routing based on wildcard pattern matching.**

📌 **Rules:**

* `*` matches **one word**
* `#` matches **zero or more words**
  Words are separated by `.`

Example routing keys:

* `user.created`
* `order.placed.india.online`

### **Diagram:**

```
Binding key: "user.*"
Routing key: "user.login" → Match

Binding key: "order.#"
Routing key: "order.india.cash" → Match
```

### **Practical Example**

Queues:

* Queue A: binding = `order.*` → handles order.placed, order.cancelled
* Queue B: binding = `order.#` → handles all order events
* Queue C: binding = `user.*` → handles user.created, user.login

Message:

* routing key = `order.placed`
  → Goes to A and B

### **Where used:**

✔ Complex routing rules
✔ Microservices event buses
✔ Multi-region systems (`order.india`, `order.us`)
✔ Chatrooms (`chat.room1`, `chat.room2`)

Topic exchange is the **most powerful** and most used.

---

# 4️⃣ **Headers Exchange**

### **Routing based on message headers instead of routing key.**

📌 **Rule:**
Match happens using the **header key/value pairs**, not routing key.

Bindings specify:

* `x-match = all` → header must match all pairs
* `x-match = any` → match any one

### **Diagram:**

```
Message headers:
type=pdf, format=A4

Queue binding:
x-match=all, type=pdf, format=A4     → Gets message
```

### **Example:**

For a document processing system:

* Queue A wants: `type=pdf`
* Queue B wants: `type=doc`
* Queue C wants: `region=india`

If message has header:

```
{ type=pdf, region=india }
```

Message goes to queues that match rules.

### **Where used:**

✔ When routing key is not flexible
✔ When metadata-based filtering needed
✔ Enterprise integrations

---

# 🧠 **Quick Summary Table**

| Exchange Type | Routing Logic                | Best Use Case                       |
| ------------- | ---------------------------- | ----------------------------------- |
| **Direct**    | Exact routing key match      | Notifications, simple microservices |
| **Fanout**    | Send to all queues           | Broadcasting, events                |
| **Topic**     | Wildcard matching (`*`, `#`) | Complex routing, event bus          |
| **Headers**   | Match on headers             | Enterprise systems, metadata-based  |

---

# 🎯 Which exchange should YOU choose?

* If you need **simple routing** → Direct
* If you need **broadcasting** → Fanout
* If you need **flexible routing** → Topic
* If you need **metadata-based routing** → Headers

