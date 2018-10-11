#include <SPI.h>
#include <MFRC522.h>
   
#define SS_PIN          15
#define RST_PIN         0

MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::StatusCode status;
  
uint8_t pageAddr = 0x06; 
  
void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("Sketch has been started!");
}

void loop() {
  
  if ( ! mfrc522.PICC_IsNewCardPresent())
    return;

  if ( ! mfrc522.PICC_ReadCardSerial())
    return;

  Serial.print(F("Card UID:"));    //Dump UID
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
  }
  Serial.println();
  Serial.println();

  Serial.setTimeout(20000L);

  byte buffer1[18];
  byte buffer2[18];
  byte size1 = sizeof(buffer1);
  byte size2 = sizeof(buffer2);
  byte len1;
  byte len2;

  memcpy(buffer1,"Fabian         ",16);
  memcpy(buffer2,"Geiselhart     ",16);
  
  Serial.println(F("Eingabe Vorname, endend mit #"));
  len1 = Serial.readBytesUntil('#', (char *) buffer1, 16);
  for (byte i = len1; i < 16; i++) buffer1[i] = ' ';

  Serial.println(F("Eingabe Nachname, endend mit #"));
  len2 = Serial.readBytesUntil('#', (char *) buffer2, 16);
  for (byte i = len2; i < 16; i++) buffer2[i] = ' ';


  // Write data Vorname ***********************************************
  pageAddr = 0x06;
  for (int i=0; i < 4; i++) { // Page 6 - 9
    //data is writen in blocks of 4 bytes (4 bytes per page)
    //Serial.println(pageAddr+i);
    status = (MFRC522::StatusCode) mfrc522.MIFARE_Ultralight_Write(pageAddr+i, buffer1 + (i*4), 4);
    if (status != MFRC522::STATUS_OK) {
      Serial.print(F("MIFARE_Read() failed: "));
      Serial.println(mfrc522.GetStatusCodeName(status));
      return;
    }
  }

  // Write data Nachname ***********************************************
  pageAddr = 0x06;
  for (int i=0; i < 4; i++) { // Page 10 - 13
    //data is writen in blocks of 4 bytes (4 bytes per page)
    //Serial.println(pageAddr+i);
    status = (MFRC522::StatusCode) mfrc522.MIFARE_Ultralight_Write(pageAddr+i+4, buffer2 + (i*4), 4);
    if (status != MFRC522::STATUS_OK) {
      Serial.print(F("MIFARE_Read() failed: "));
      Serial.println(mfrc522.GetStatusCodeName(status));
      return;
    }
  }

  Serial.println(F("======= SUCCESS ======="));
  Serial.println();

  byte readbuffer1[18]; 
  byte readbuffer2[18];

  // Read data Vorname ***************************************************
  Serial.println(F("Reading data ... "));
  //data in 4 block is readed at once.
  status = (MFRC522::StatusCode) mfrc522.MIFARE_Read(6, readbuffer1, &size1);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("MIFARE_Read() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }
  status = (MFRC522::StatusCode) mfrc522.MIFARE_Read(10, readbuffer2, &size2);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("MIFARE_Read() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  Serial.print(F("Readed data: "));
  //Dump a byte array to Serial
  for (byte i = 0; i < 16; i++) {
    Serial.write(readbuffer1[i]);
  }
  for (byte i = 0; i < 16; i++) {
    Serial.write(readbuffer2[i]);
  }
  Serial.println();
  Serial.println();
  Serial.println(F("======= SUCCESS ======="));
  Serial.println();

  mfrc522.PICC_HaltA();

}
