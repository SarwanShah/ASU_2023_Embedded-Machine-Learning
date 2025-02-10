# 🌬️ Wind Speed Estimation on an Embedded System using Closely Spaced Microphones

## 📌 Project Overview
This project was developed under the **CEN 598: Embedded Machine Learning** course at **Arizona State University** during Fall 2023. The goal was to estimate wind speed using **audio data** from two closely spaced microphones on an **ESP32** embedded system, leveraging machine learning to analyze **wind noise** correlation.

**REPORT**: [Final Project Report](./Final%20Project%20Report.pdf)  
**PRESENTATION**: [Project Presentation](./CEN598-FinalProjectPresentation-SarwanShah.pptx)

---

## **🌟 Motivation**
- **Meteorological Data Sparsity**: Accurate weather predictions require denser data networks, which current **Automatic Weather Stations (AWS)** struggle to provide at scale due to cost and infrastructure.
- **Low-Cost Wind Estimation**: This project explores the feasibility of **deploying microphone-based wind speed sensors** in scalable, cost-effective solutions.
- **Future Applications**: Enabling weather-sensitive devices like smartphones or cars to include wind estimation as a feature.

---

## **🛠 Features**
- **Hardware Setup**:
  - **ESP32 Microcontroller** with **I2S peripherals** for audio data processing.
  - **INMP441 MEMs Microphones** capturing wind noise across two channels.
  - **Hall-Effect Anemometer** for ground-truth wind speed labels.
  - **DHT11 Sensor** for temperature and humidity data collection.

- **Data Collection**:
  - Gathered over **5000 samples** across 10 fan speeds, varying microphone directions for broader dataset coverage.
  - Audio sampled at **1 kHz**, 16-bit format.

- **Machine Learning Model**:
  - Spectrograms generated from audio samples to visualize frequency components below **51 Hz**.
  - Trained a **Convolutional Neural Network (CNN)** to predict wind speed.

---

## **📊 Implementation Highlights**
### ➤ **Data Collection**
- Samples were gathered using a controlled fan and multiple directions to explore classification potential.
- ESP32 managed stereo microphone inputs, streamed to a PC via serial communication.

### ➤ **Training Process**
- **Preprocessing**: 
  - Data was normalized using **min-max scaling**.
  - Spectrograms generated from both microphone channels.
  
- **Model Architecture**:
  - **CNN** with dropout layers to address overfitting.
  - Input: Paired spectrograms from the two microphones.
  - Output: Estimated wind speed in meters per second.

- **Challenges**:
  - Difficulties in maintaining high audio sampling rates due to embedded system limitations.
  - Overfitting observed in training, requiring further feature engineering.

---

## **📈 Results**
- The model showed signs of learning from frequency differences between spectrograms at various wind speeds.
- However, results were inconclusive without further data and experimentation.
  
---

## **🔮 Future Work**
- Improve data collection efficiency and increase dataset size.
- Experiment with feature extraction techniques to enhance model learning.
- Explore classification tasks using directional microphone data.
  
---

## **📥 How to Use**
1. Connect the **ESP32** with microphones and sensors as per the provided circuit configuration.
2. Run the **data collection script** to gather samples.
3. Train the machine learning model using the provided **Colab notebook**.
4. Evaluate the model with the generated test data.
