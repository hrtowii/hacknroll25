import { useState, useEffect, useCallback, useRef } from 'react';
import { NextUIProvider, Card, Button, Input, Spacer } from "@nextui-org/react";
import { Send } from 'lucide-react';
import { ChatMessage } from './components/Chat';
import { WebcamCapture } from './components/WebcamCapture';
import Webcam from 'react-webcam';
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
  const webcamRef = useRef<Webcam>(null);

  // Capture function to get screenshot from webcam
  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      setImage(imageSrc); // Save the captured image
      console.log(imageSrc)
      console.log("image captured");
    }
  }, [webcamRef]);

  // Function to toggle timer
  const toggleCapture = () => {
    setIsCapturing(prev => !prev);
  };

  // Effect to handle periodic capturing
  useEffect(() => {
    let timer: ReturnType<typeof setInterval> | null = null;

    if (isCapturing) {
      timer = setInterval(() => {
        capture();
      }, 5000); // Capture every 5 seconds
    }

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
        <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-2 bg-white rounded-2xl p-4 shadow-lg flex flex-col h-[80vh]">
            <div className="flex-1 overflow-y-auto space-y-4 p-4">
              {messages.map((message, index) => (
                <ChatMessage key={index} message={message.text} isAI={message.isAI} />
              ))}
            </div>
            <div className="p-4 border-t">
              <div className="flex gap-2">
                <Input
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Type your message..."
                  endContent={
                    <Button
                      isIconOnly
                      color="primary"
                      variant="flat"
                      onPress={handleSendMessage}
                    >
                      <Send size={20} />
                    </Button>
                  }
                />
              </div>
            </div>
          </div>
          <div className="flex flex-col gap-4">
            <Card style={{ width: '300px', padding: '20px' }}>
              <Webcam
                audio={false}
                mirrored={true}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                className="rounded-lg w-full"
              />
              {image && (
                <div>
                  <h4>Captured Image:</h4>
                  <img src={image} alt="Captured" style={{ width: '100%', marginTop: '10px' }} />
                </div>
              )}
              <Spacer y={1} />
              <Button onClick={toggleCapture}>
                {isCapturing ? 'Stop Capture' : 'Start Capture'}
              </Button>
              <Spacer y={1} />
              <Button onClick={analyzeImage}>Analyze Emotion</Button>
              <Spacer y={1} />
              <Button onClick={roastUser}>Roast Me</Button>
            </Card>
            <div className="bg-white rounded-2xl p-4 shadow-lg">
              <h3 className="text-lg font-semibold mb-2">Current Emotion</h3>
              <p className="text-gray-600">{emotion || 'Waiting for emotion detection...'}</p>
            </div>
            <Duck emotion={emotion} />
          </div>
        </div>
      </div>
    </NextUIProvider>
  );
}

export default App;