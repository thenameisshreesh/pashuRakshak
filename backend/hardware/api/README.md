# Hardware Verification API

This API endpoint is exposed by the Flask backend specifically for consumption by ESP32 edge scanning devices.

## 1. Scan Tag Entry

Submit a scanned RFID tag ID during an active verification session.

* **Endpoint:** `/api/scanning/tag`
* **Method:** `POST`
* **Content-Type:** `application/json`
* **Headers:**
  * `Authorization: Bearer <device_access_token>`

### Request Body

```json
{
  "session_id": "60d5ec4b1f3c2c2b3d8b4567",
  "tag_id": "RFID_TAG_987654321012"
}
```

### Success Response (200 OK)

```json
{
  "success": true,
  "message": "Tag scanned and verified",
  "data": {
    "cattle_id": "60d5ec4b1f3c2c2b3d8b9999",
    "farmer_name": "Ramesh Kumar",
    "verification_status": "verified"
  }
}
```

### Error Responses

* **401 Unauthorized:** Invalid or missing Bearer token.
* **404 Not Found:** Active scanning session or cattle tag ID not found.
* **400 Bad Request:** Missing required fields (`session_id`, `tag_id`).
