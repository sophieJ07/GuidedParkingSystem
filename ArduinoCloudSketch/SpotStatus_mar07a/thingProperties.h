#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>

const char SSID[]     = SECRET_SSID;    // Network SSID (name)
const char PASS[]     = SECRET_OPTIONAL_PASS;    // Network password (use for WPA, or use as key for WEP)

void onSpot1Change();
void onSpot2Change();
void onSpot3Change();
void onSpot4Change();
void onSpot5Change();

bool spot1;
bool spot2;
bool spot3;
bool spot4;
bool spot5;

void initProperties(){

  ArduinoCloud.addProperty(spot1, READWRITE, ON_CHANGE, onSpot1Change);
  ArduinoCloud.addProperty(spot2, READWRITE, ON_CHANGE, onSpot2Change);
  ArduinoCloud.addProperty(spot3, READWRITE, ON_CHANGE, onSpot3Change);
  ArduinoCloud.addProperty(spot4, READWRITE, ON_CHANGE, onSpot4Change);
  ArduinoCloud.addProperty(spot5, READWRITE, ON_CHANGE, onSpot5Change);

}

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);
