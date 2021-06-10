#include <Arduino.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <Ticker.h>
#include <EEPROM.h>

#ifndef STASSID
#define SSID "Sina behnam"
#define STAPSK "1144800s"
#endif

#define MAGIC_NUMBER 42

const char * ssid = SSID;
const char * psk = STAPSK;

const byte interruptPin = 12; //(e.g) gas detector

WiFiClient client;

HTTPClient http;

String Host="192.168.43.213"; //my desktop local address can be 192.168.43.213 or 192.168.1.5 or 192.168.137.201

uint16_t port = 8000;

Ticker auth_ticker,update_ticker;

void ICACHE_RAM_ATTR interrupt_handler_00(); //for interrupt handeling
volatile bool interrupt_handler_00_flage = false;

struct Auth_Token
{
  String access = "";
  String refresh = "";
}auth_token;

struct IPConfig
{
  IPAddress local;
  IPAddress dns;
  IPAddress gate_way;
}ip_config;

struct RestInfo
{
  int magic = MAGIC_NUMBER;
  int rest_number = 0;
}rest_info;

bool Authentication(){
  bool has_auth = false;
  DynamicJsonDocument doc(200);

  doc["email"] = "sina.behnam.ac@gmail.com";
  doc["password"] = "114480";

  String json;
  serializeJsonPretty(doc,json);
  http.useHTTP10(true);
  if(http.begin(client,Host,port,"/users/signin/")){
    http.addHeader("Content-Type", "application/json");
    Serial.print("[HTTP] POST...\n");

    int httpCode = http.POST(json);

    if(httpCode > 0){
      Serial.printf("[HTTP] POST... code: %d\n",httpCode);

      if(httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY){
        has_auth = true;
        Serial.println("Authorization responce : \n");

        DynamicJsonDocument payload(800);
        deserializeJson(payload,http.getStream());

        Serial.print("access_token : \n");
        auth_token.access = payload["access_token"].as<String>();
        Serial.println(auth_token.access);
        Serial.print("refresh_token : \n");
        auth_token.refresh = payload["refresh_token"].as<String>();
        Serial.println(auth_token.refresh);

        JsonObject user = payload["user"].as<JsonObject>();

        Serial.print("email : ");
        Serial.println(user["email"].as<String>());
      }
    }
    else{
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end();
  }
  else{
    Serial.printf("[HTTP] Unable to connect\n");
  }
  return has_auth;
}

void auth_driver(){
  if(!Authentication()){
    Serial.println("Authentication Failed\n");
  }else{
    Serial.println("Authentication Successfully\n");
  }
}

bool Save_IP_Config(IPConfig config){
  EEPROM.put(0,config);
  if(EEPROM.commit()){
    Serial.println("\nip setting saved successfully\n");
    // WiFi.config(config.local,config.gate_way,24,config.dns);
    return true;
  }else{
    Serial.println("\n can not write in EEPROM memory !!\n");
    return false;
  }
}

void UpdateESP(){
  http.useHTTP10(true);
  String message = "/boards/esp/";
  message += String(ESP.getChipId());
  if(http.begin(client,Host,port,message)){
    String token = "Bearer ";
    token += auth_token.access;
    http.addHeader("Authorization",token);
    http.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] GET...\n");

    int httpCode = http.GET();
    if(httpCode > 0){
      Serial.printf("[HTTP] GET... code: %d\n",httpCode);
      
      DynamicJsonDocument payload(1024);
      deserializeJson(payload,http.getStream());
      if(httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY){
        Serial.println("Updated Successfully : \n");
        ip_config.local.fromString(payload["local_ip_address"].as<String>());
        ip_config.dns.fromString(payload["DNS_ip_address"].as<String>());
        ip_config.gate_way.fromString(payload["getAway_ip_address"].as<String>());
        Save_IP_Config(ip_config);
      }else{
        serializeJsonPretty(payload,Serial);
      }
    }
    else{
      Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
  http.end();
  }else{
    Serial.printf("[HTTP] Unable to connect\n");
  }
}

void update_driver(){
  UpdateESP();
}

void ESP_Details(){
  DynamicJsonDocument doc(1024);

  doc["name"] = "NodeMcu-12E";
  doc["flash_free_space"] =  ESP.getFlashChipSize() - ESP.getSketchSize();
  doc["ram_free_space"] =  ESP.getFreeHeap();
  doc["rest_number"] =  rest_info.rest_number;
  doc["mac_address"] =  WiFi.macAddress();
  doc["local_ip_address"] =  ip_config.local;
  doc["getAway_ip_address"] =  ip_config.gate_way;
  doc["DNS_ip_address"] =  ip_config.dns;
  doc["SSID_name"] =  SSID;
  doc["core_version"] =  ESP.getCoreVersion();
  doc["sdk_version"] =  ESP.getSdkVersion();
  doc["cpu_freq_mHz"] =  String(ESP.getCpuFreqMHz());
  doc["flash_chip_id"] =  String(ESP.getFlashChipId());
  doc["rest_reason"] =  ESP.getResetReason();

  String json;
  serializeJsonPretty(doc,json);
  http.useHTTP10(true);
  String message = "/boards/esp/";
  message += String(ESP.getChipId());
  if(http.begin(client,Host,port,message)){
    String token = "Bearer ";
    token += auth_token.access;
    http.addHeader("Authorization",token);
    http.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] PUT...\n");

    int httpCode = http.PUT(json);

    if(httpCode > 0){
      Serial.printf("[HTTP] PUT... code: %d\n",httpCode);
      
      DynamicJsonDocument payload(600);
      deserializeJson(payload,http.getStream());
      if(httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY){
        Serial.println("Sending Details Successfully : \n");
      }else{
        serializeJsonPretty(payload,Serial);
      }
    }
    else{
      Serial.printf("[HTTP] PUT... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end();
  }
  else{
    Serial.printf("[HTTP] Unable to connect\n");
  }
}

void Set_IP_Config(){
  if(rest_info.rest_number==1){
    ip_config.local.fromString("192.168.43.130");
    ip_config.gate_way.fromString("192.168.43.1");
    ip_config.dns.fromString("192.168.43.1");
    //for the fisrt time it has to set to default configuration  
    Save_IP_Config(ip_config);
  }else{
    EEPROM.get(0,ip_config);
  }
  Serial.println(ip_config.local);
  Serial.println(ip_config.gate_way);
  Serial.println(ip_config.dns);
  IPAddress subnet(255,255,255,0);
  if(WiFi.config(ip_config.local,ip_config.gate_way,subnet,ip_config.dns)){
    Serial.println("Connection configured");
  }
}

void send_analog_data(String token){
  
}

void Send_Emergency_Request(String token,DynamicJsonDocument document){

  String json;
  serializeJsonPretty(document,json);
  http.useHTTP10(true);
  String message = "/boards/esp/sensors/";
  message += String(ESP.getChipId());
  if(http.begin(client,Host,port,message)){
    String token = "Bearer ";
    token += auth_token.access;
    http.addHeader("Authorization",token);
    http.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] POST...\n");

    int httpCode = http.POST(json);

    if(httpCode > 0){
      Serial.printf("[HTTP] POST... code: %d\n",httpCode);
      
      DynamicJsonDocument payload(600);
      deserializeJson(payload,http.getStream());
      if(httpCode == HTTP_CODE_CREATED || httpCode == HTTP_CODE_MOVED_PERMANENTLY){
        Serial.println("Sending Sensor's data Successfully : \n");
      }else{
        Serial.println("Sending Sensor's data Occured with ERROR : \n");
      }
      serializeJsonPretty(payload,Serial);  
    }
    else{
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end();
  }
  else{
    Serial.printf("[HTTP] Unable to connect\n");
  }
}



volatile unsigned long previousMillis = 0;
volatile const long interval = 250;


void setup() {
  Serial.begin(115200);
  EEPROM.begin(1024);
  Serial.println();
  delay(1000);
  attachInterrupt(digitalPinToInterrupt(interruptPin), interrupt_handler_00, RISING);
  EEPROM.get(1000,rest_info);
  if(rest_info.magic != MAGIC_NUMBER){
    rest_info.magic = MAGIC_NUMBER;
    rest_info.rest_number=0; // initialize for first time
    Serial.printf("\n#######################################################\n");    
    Serial.printf("This is the first time!!! the number is initialize to 0\n");    
    Serial.printf("#######################################################\n");  
  }
  rest_info.rest_number++;
  EEPROM.put(1000,rest_info);
  Serial.printf("Connecting to  %s : ", ssid);
  Serial.print("\n");
  Set_IP_Config();
  WiFi.begin(ssid, psk);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.print("\n");
  Serial.print("Local ip address : ");
  Serial.println(WiFi.localIP());
  Serial.println("Connected to Access point");

  delay(100);
  if(Authentication()){
    ESP_Details();
    update_ticker.attach_scheduled(30,update_driver);
    auth_ticker.attach_scheduled(300,auth_driver);
  }else{
    Serial.println("Authentication Failed\n");
  }
}

void loop() {
  if(interrupt_handler_00_flage){
    interrupt_handler_00_flage = false;
    DynamicJsonDocument doc(500);
    doc["name"] = "gas detection";
    doc["type"] = "INTERRUPTION_00";
    doc["status"] = "Warning";
    doc["message"] = "some thing on fire";
    JsonObject sensor_data = doc.createNestedObject("data");
    sensor_data["pin"] = interruptPin;
    sensor_data["interrupt_action"] = "RISING";

    Send_Emergency_Request(auth_token.access,doc);
  }
  
}

void interrupt_handler_00(){
  volatile unsigned long currentMillis = millis(); 
  if (currentMillis - previousMillis >= interval) {
  previousMillis = currentMillis;
  interrupt_handler_00_flage = true;
  Serial.println("Gas detected !!!");
  }
}