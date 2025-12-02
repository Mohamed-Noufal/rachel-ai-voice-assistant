# Chat with Rachel - Voice Chat Application
 
A full-stack voice chat application built with React, FastAPI, and AI services that enables voice-based conversations with an AI assistant named Rachel.
 
## 🌟 Features
 
- Real-time voice recording and playback
- Speech-to-text conversion using Whisper
- AI-powered chat responses using Groq API
- Text-to-speech conversion using ElevenLabs
- Modern, responsive UI built with React and Tailwind CSS
- FastAPI backend with robust error handling

## 🛠️ Tech Stack

### Frontend
- React with TypeScript
- Tailwind CSS for styling
- Vite as build tool
- Axios for API calls

### Backend
- FastAPI (Python)
- Whisper for speech-to-text
- Groq API for chat responses
- ElevenLabs for text-to-speech
- CORS middleware for cross-origin requests

## 📋 Prerequisites

- Node.js and npm
- Python 3.x
- FFmpeg
- API keys for:
  - Groq API
  - ElevenLabs

## 🚀 Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file with:
   ```
   GROQ_API_KEY=your_groq_api_key
   ELEVEN_LABS_API_KEY=your_eleven_labs_api_key
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend/chat-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## 🎯 Usage

1. Open the application in your browser (typically at http://localhost:5173)
2. Click the microphone button to start recording
3. Speak your message
4. Release the button to send your message
5. Wait for Rachel's voice response

## 📝 API Endpoints

- `GET /` - Root endpoint
- `GET /reset` - Reset conversation
- `POST /post-audio/` - Process audio and get AI response
- `GET /post-audio-get/` - Alternative endpoint for audio processing

## 💡 Use Cases

### 1. Customer Support
- **24/7 Availability**: Provide round-the-clock customer support without human limitations
- **Instant Response**: Eliminate wait times with immediate voice-based responses
- **Multilingual Support**: Potential to handle customer queries in multiple languages
- **Consistent Service**: Maintain uniform quality in responses across all interactions
- **Cost-Effective**: Reduce operational costs while scaling support capabilities

### 2. Clinical Assistant
- **Patient Screening**: Help with initial patient symptom assessment
- **Appointment Scheduling**: Handle booking and rescheduling through natural voice conversations
- **Medical Information**: Provide basic medical information and health guidelines
- **Medication Reminders**: Assist patients with medication schedules and instructions
- **Healthcare Access**: Improve accessibility to basic healthcare information for remote areas

### 3. Educational Support
- **24/7 Tutoring**: Provide constant learning support for students
- **Language Learning**: Practice conversations in foreign languages
- **Homework Help**: Assist with explanations and problem-solving
- **Accessibility**: Support students with reading or writing difficulties

## 🌍 Impact on Our World

### Transforming Customer Experience
- **Humanized Interactions**: Voice-based AI creates more natural and engaging customer experiences
- **Accessibility**: Makes services available to people who struggle with typing or reading
- **Efficiency**: Reduces wait times and improves service availability
- **Data-Driven Insights**: Helps businesses understand customer needs better through conversation analytics

### Revolutionizing Healthcare
- **Improved Access**: Makes basic healthcare information more accessible to everyone
- **Reduced Burden**: Helps healthcare providers by handling routine queries
- **Early Screening**: Assists in preliminary health assessments
- **Patient Education**: Provides reliable health information in an interactive format

### Advancing Education
- **Personalized Learning**: Adapts to individual learning paces and styles
- **Immediate Support**: Provides instant help when human tutors aren't available
- **Inclusive Education**: Supports different learning abilities and preferences
- **Global Reach**: Makes educational support available regardless of location

### Environmental Impact
- **Reduced Travel**: Fewer in-person visits needed for basic services
- **Paper Reduction**: Less reliance on printed materials
- **Resource Efficiency**: Optimal use of human resources in service industries

### Future Implications
- **AI Integration**: Paves the way for more sophisticated AI-human interactions
- **Skill Evolution**: Shifts focus to more complex human-centric tasks
- **Service Democracy**: Makes professional services more accessible to everyone
- **Innovation Driver**: Encourages development of more advanced AI applications

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
