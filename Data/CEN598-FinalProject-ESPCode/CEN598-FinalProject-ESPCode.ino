#include <driver/i2s.h>
#include <Arduino.h>
#include "DHT_Async.h"

// Define pins for I2S communication
#define I2S_WS 21
#define I2S_SD 22
#define I2S_SCK 23

// Define pins and type for DHT sensor
#define DHT_SENSOR_TYPE DHT_TYPE_11
static const int DHT_SENSOR_PIN = 20;
DHT_Async dht_sensor(DHT_SENSOR_PIN, DHT_SENSOR_TYPE);

// Variables for debouncing interrupt
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 1000;    // the debounce time; increase if the output flickers
int pinInterrupt = 19;
int Count = 0;

// I2S configuration
#define I2S_PORT I2S_NUM_0
#define bufferLen 1024

float temperature_ = 0.0;
float humidity_ = 0.0;
float windSpeed = 0.0;
int sampleNumber = 0;

// Double the buffer size for stereo data
int16_t sBuffer[bufferLen * 2];

// Function to install I2S driver
void i2s_install() {
  const i2s_config_t i2s_config = {
    .mode = i2s_mode_t(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = 1000,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,  // Set to LEFT for left channel
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = 0,
    .dma_buf_count = 8,
    .dma_buf_len = bufferLen,
    .use_apll = false
  };

  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
}

// Function to set I2S pins
void i2s_setpin() {
  const i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD
  };

  i2s_set_pin(I2S_PORT, &pin_config);
}

void setup() {
  Serial.begin(115200);
  Serial.println(" ");
  delay(10000);
  pinMode(pinInterrupt, INPUT_PULLUP);// set the interrupt pin
  attachInterrupt(digitalPinToInterrupt(pinInterrupt), onChange, FALLING);

  // Initialize and start I2S
  i2s_install();
  i2s_setpin();
  i2s_start(I2S_PORT);
  delay(100);
  Serial.println("SAMPLE,WIND_SPEED,MIC_A,MIC_B");
  delay(500);
}

void loop() {
  // Debounce and calculate wind speed
  if ((millis() - lastDebounceTime) > debounceDelay) {
      windSpeed = (float)(Count * 8.75)/(float)100.0;
      lastDebounceTime = millis();
      sampleNumber += 1;
      Count = 0;
  }
  
  // Read from I2S and print data
  size_t bytesIn = 0;
  esp_err_t result = i2s_read(I2S_PORT, &sBuffer, bufferLen * 2, &bytesIn, portMAX_DELAY);

  if (result == ESP_OK) {
    int16_t samples_read = bytesIn / 4;  // Each sample is 16 bits (2 bytes)
    if (samples_read > 0) {
      for (int16_t i = 0; i < samples_read; i += 2) {
        Serial.print(sampleNumber);
        Serial.print(",");
        Serial.print(windSpeed);
        Serial.print(",");
        Serial.print(sBuffer[i]);
        Serial.print(",");
        Serial.println(sBuffer[i + 1]);
      }
    }
  }  
}

// Function to measure temperature and humidity using DHT sensor
static bool measure_environment(float *temperature, float *humidity) {
    static unsigned long measurement_timestamp = millis();

    // Measure once every four seconds
    if (millis() - measurement_timestamp > 1000ul) {
        if (dht_sensor.measure(temperature, humidity)) {
            measurement_timestamp = millis();
            return (true);
        }
    }

    return (false);
}

// Interrupt handler for pin change
void onChange() {
  if (digitalRead(pinInterrupt) == LOW )
    Count++;
}
