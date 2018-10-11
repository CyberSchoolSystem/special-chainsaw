/* mifare ultralight example (25-02-2018)
 * 
 *   RFID-RC522 (SPI connexion)
 *   
 *   CARD RC522      Arduino (UNO)
 *     SDA  -----------  10 (Configurable, see SS_PIN constant)
 *     SCK  -----------  13
 *     MOSI -----------  11
 *     MISO -----------  12
 *     IRQ  -----------  
 *     GND  -----------  GND
 *     RST  -----------  9 (onfigurable, see RST_PIN constant)
 *     3.3V ----------- 3.3V
 *     
 */

  #include <SPI.h>
  #include <MFRC522.h>
  #include <Keyboard.h>
  
  
  #define SS_PIN          10
  #define RST_PIN         5

  #define KEY_RETURN 0xB0

  MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance
  MFRC522::StatusCode status; //variable to get card status
  
  byte buffer1[18];  //data transfer buffer (16+2 bytes data+CRC)
  byte buffer2[18];
  byte size1 = sizeof(buffer1);
  byte size2 = sizeof(buffer2);

  uint8_t pageAddr = 0x06;  //In this example we will write/read 16 bytes (page 6,7,8 and 9).
                            //Ultraligth mem = 16 pages. 4 bytes per page.  
                            //Pages 0 to 4 are for special functions.           
  
void setup() {
  Keyboard.begin(); // Initialize serial communications with the PC
  SPI.begin(); // Init SPI bus
  mfrc522.PCD_Init(); // Init MFRC522 card  
  Serial.println(F("Warte auf Tag!"));
}

void loop() {
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent())
    return;

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial())
    return;

  Serial.println(F("======= SUCCESS ======="));
  Serial.println();

  byte readbuffer1[18]; 
  byte readbuffer2[18];

  // Read data Vorname ***************************************************
  //Serial.println(F("Reading data ... "));
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
    if(readbuffer1[i] != 32){
      Keyboard.write(readbuffer1[i]);
    }
  }
  Keyboard.print(".");
  for (byte i = 0; i < 16; i++) {
    Serial.write(readbuffer2[i]);
    if(readbuffer2[i] != 32){
      Keyboard.write(readbuffer2[i]);
    }
  }

Keyboard.write(KEY_RETURN);
  
  Serial.println();
  Serial.println();
  Serial.println();  

  mfrc522.PICC_HaltA();

  memset(readbuffer1, 0, sizeof(readbuffer1));
  memset(readbuffer2, 0, sizeof(readbuffer2));
}
