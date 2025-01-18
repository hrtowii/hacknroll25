import { useState, useEffect, useCallback, useRef } from 'react';
import { NextUIProvider, Button, Input, Spacer } from "@nextui-org/react";
import { Send } from 'lucide-react';
import { ChatMessage } from './components/Chat';
import Duck from './components/Duck';

interface Message {
  text: string;
  isAI: boolean;
}

function App() {
  const [emotion, setEmotion] = useState('');
  const [drowsiness, setDrowsiness] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hey there! I'm your personal roasting AI. Turn on your camera so I can see your beautiful face and roast you properly! 😈", isAI: true }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [image, setImage] = useState<string | null>(null);
  const [isCapturing, setIsCapturing] = useState(false); // Track whether capturing is active
  const webcamRef = useRef<any>(null);

  // Capture function to get screenshot from webcam
  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      setImage(imageSrc); // Save the captured image
      console.log(imageSrc)
      console.log("image captured");
    }
  }, [webcamRef]);

  // Effect to handle periodic capturing
  useEffect(() => {
    let timer: ReturnType<typeof setInterval> | null = null;

    timer = setInterval(() => {
      capture();
    }, 5000); // Capture every 5 seconds

    return () => {
      if (timer) {
        clearInterval(timer);
      }
    };
  }, [isCapturing, capture]);

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    setMessages(prev => [...prev, { text: inputMessage, isAI: false }]);
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        text: "I see you're trying to chat. That's adorable. Almost as adorable as your attempt at a serious face right now! 😏", 
        isAI: true 
      }]);
    }, 1000);
    setInputMessage('');
  };

  const roastUser = async () => {
    if (!image) return;

    const response = await fetch('http://localhost:5000/roast', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image }),
    });

    const data = await response.json();
    setMessages(prev => [...prev, { text: `Roast: ${data.roast}`, isAI: true }]);
  };

  const analyzeImage = async () => {
    if (!image) return;

    const response = await fetch('http://localhost:5000/detect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ frame: image.split(',')[1] }),
    });

    const data = await response.json();
    setEmotion(data.emotion);
    setDrowsiness(data.drowsiness);
    setMessages(prev => [...prev, { text: `Emotion: ${data.emotion}, Drowsiness: ${data.drowsiness}`, isAI: true }]);
  };

  return (
    <NextUIProvider>
  <div className="min-h-screen bg-gradient-to-br from-yellow-500 to-orange-800 p-4">
    <div className="flex flex-col items-center gap-4">
      {/* Duck Component */}
      <Duck emotion={emotion} />

      {/* Message Area */}
      <div className="bg-white rounded-2xl p-4 shadow-lg flex flex-col w-full">
        <div className="flex-1 overflow-y-auto space-y-4 p-4">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message.text} isAI={message.isAI} />
          ))}
        </div>
      </div>

      {/* Buttons to Analyze Image and Roast */}
      <div className="flex flex-col gap-4 w-full mt-4">
        <Button onClick={analyzeImage} className="w-full">Analyze Emotion</Button>
        <Button onClick={roastUser} className="w-full">Roast Me</Button>
      </div>

      {/* Emotion Display */}
      <div className="bg-white rounded-2xl p-4 shadow-lg w-full mt-4">
        <h3 className="text-lg font-semibold mb-2">Current Emotion</h3>
        <p className="text-gray-600">{emotion || 'Waiting for emotion detection...'}</p>
      </div>
    </div>
  </div>
</NextUIProvider>



  );
}

export default App;
