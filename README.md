# Clip-Away-Producer
![Python](https://img.shields.io/badge/python-3.10-blue)
![Vercel](https://img.shields.io/badge/vercel-deployed-black)
![Azure](https://img.shields.io/badge/azure-enabled-blue)
![MessageNX](https://img.shields.io/badge/messagenx-enabled-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

**Clip Away** is an AI-powered background removal tool that automates image cutouts using the **rembg** library with the **U2NetP** deep learning model. It is hosted on **AWS EC2** and integrates with **MessageNX**, a lightweight producer-consumer messaging library, to handle image processing tasks asynchronously.

---

## Features

- Real-time background removal with high accuracy  
- Hosted on **Azure Web App** for scalable cloud processing  
- Asynchronous image processing using **MessageNX**  
- Supports batch image processing  
- Lightweight and easy to integrate into Python applications  

---

## How It Works

### 1. Producer – Handling Client Requests

The **Producer** receives image requests from clients and pushes them into a **MessageNX channel** for processing.

**Workflow:**
1. Client uploads an image via a web or mobile interface.  
2. The Producer packages the image into a **message object**:
```json
{
  "image": "input.jpg",
  "user_id": "12345",
  ..........
}
