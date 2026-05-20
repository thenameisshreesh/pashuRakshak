/**
 * PashuRakshak RFID Scanner - ESP32 Firmware
 * 
 * This firmware reads UIDs from standard RFID tags using the MFRC522 reader via SPI,
 * connects to local Wi-Fi, and sends an HTTP POST request containing the tag ID and 
 * scanning session ID to the Flask backend.
 * 
 * Required Arduino Libraries:
 * - MFRC522 (by GithubCommunity)
 * - ArduinoJson (by Benoit Blanchon)
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <SPI.h>
#include <MFRC522.h>
#include <ArduinoJson.h>

// Wi-Fi Credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Server Configuration
// Change this to your backend IP or Domain
// When running locally, use your computer's local IP (e.g. 192.168.1.100) instead of localhost/127.0.0.1
const char* backendUrl = "http://192.168.1.100:5000/api/scanning/tag";
const char* sessionId = "YOUR_SESSION_ID"; // Set the active scan session ID from the web portal/mobile app

// ESP32 Pins for MFRC522 (SPI Interface)
#define SS_PIN    5   // VSPI CS / SDA Pin
#define RST_PIN   22  // Reset Pin
#define LED_PIN   2   // Onboard LED for status indicators

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Initialize SPI bus
  SPI.begin();
  
  // Initialize MFRC522 reader
  mfrc522.PCD_Init();
  Serial.println("PashuRakshak RFID Scanner Initialized.");
  Serial.print("MFRC522 Digital self test: ");
  mfrc522.PCD_DumpVersionToSerial();
  
  // Connect to Wi-Fi
  connectToWiFi();
}

void loop() {
  // Check Wi-Fi connection status
  if (WiFi.status() != WL_CONNECTED) {
    connectToWiFi();
  }

  // Look for new RFID cards/tags
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // Visual feedback for scan
  digitalWrite(LED_PIN, HIGH);

  // Read Card UID and convert to String representation
  String tagId = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    tagId += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
    tagId += String(mfrc522.uid.uidByte[i], HEX);
  }
  tagId.toUpperCase();

  Serial.println("\n----------------------------------------");
  Serial.print("Card Scanned! UID: ");
  Serial.println(tagId);

  // Send the tag ID to Flask Backend
  sendTagToBackend(tagId);

  // Halt PICC
  mfrc522.PICC_HaltA();
  // Stop encryption on PCD
  mfrc522.PCD_StopCrypto1();

  // Small delay and turn off LED
  delay(1000);
  digitalWrite(LED_PIN, LOW);
}

void connectToWiFi() {
  Serial.println();
  Serial.print("Connecting to Wi-Fi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  int retryCount = 0;
  while (WiFi.status() != WL_CONNECTED && retryCount < 20) {
    delay(500);
    Serial.print(".");
    // Blink LED during connection attempt
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    retryCount++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected to Wi-Fi successfully!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    digitalWrite(LED_PIN, HIGH);
    delay(1000);
    digitalWrite(LED_PIN, LOW);
  } else {
    Serial.println("\nFailed to connect to Wi-Fi. Scanner will continue running offline/retrying.");
    digitalWrite(LED_PIN, LOW);
  }
}

void sendTagToBackend(String tagId) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Error: Cannot send tag. Wi-Fi not connected.");
    return;
  }

  HTTPClient http;
  
  Serial.print("Sending POST request to: ");
  Serial.println(backendUrl);

  http.begin(backendUrl);
  http.addHeader("Content-Type", "application/json");

  // Create JSON Payload
  StaticJsonDocument<200> doc;
  doc["session_id"] = sessionId;
  doc["tag_id"] = tagId;

  String jsonString;
  serializeJson(doc, jsonString);

  Serial.print("Payload: ");
  Serial.println(jsonString);

  // Send POST Request
  int httpResponseCode = http.POST(jsonString);

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response Code: ");
    Serial.println(httpResponseCode);
    
    String responseString = http.getString();
    Serial.print("Response: ");
    Serial.println(responseString);
    
    // Parse response to display status feedback
    StaticJsonDocument<300> filter;
    filter["status"] = true;
    filter["message"] = true;
    
    StaticJsonDocument<300> responseDoc;
    DeserializationError error = deserializeJson(responseDoc, responseString);
    
    if (!error) {
      const char* status = responseDoc["status"];
      const char* message = responseDoc["message"];
      Serial.print("Tag Status: ");
      Serial.println(status ? status : "UNKNOWN");
      
      // Buzzer or LED patterns can be implemented here based on match/fraud
      if (status && strcmp(status, "matched") == 0) {
        Serial.println(">>> SUCCESS: Cattle verified. (Green Light)");
        // Blink twice quickly
        blinkLED(2, 100);
      } else if (status && strcmp(status, "suspicious") == 0) {
        Serial.println(">>> WARNING: SUSPICIOUS TAG OWNER MATCH MISMATCH! (Orange/Red Light)");
        blinkLED(5, 50);
      } else {
        Serial.println(">>> ERROR: Unmatched tag. Not allocated for this scheme.");
        blinkLED(1, 1000); // long single flash
      }
    }
  } else {
    Serial.print("Error sending POST request. HTTP Error Code: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

void blinkLED(int count, int delayMs) {
  for (int i = 0; i < count; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(delayMs);
    digitalWrite(LED_PIN, LOW);
    delay(delayMs);
  }
}
