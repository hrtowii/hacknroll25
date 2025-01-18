import { useState } from 'react';
import { NextUIProvider } from "@nextui-org/react";
import { Button, Input } from "@nextui-org/react";
import { Send } from 'lucide-react';
import { ChatMessage } from './components/Chat';
import { WebcamCapture } from './components/WebcamCapture';

interface Message {
  text: string;
  isAI: boolean;
}

function App() {
<<<<<<< Updated upstream
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hey there! I'm your personal roasting AI. Turn on your camera so I can see your beautiful face and roast you properly! 😈", isAI: true }
  ]);
  const [inputMessage, setInputMessage] = useState('');
=======
  const [emotion, setEmotion] = useState('');
  const [drowsiness, setDrowsiness] = useState('');
  const [messages, setMessages] = useState<string[]>([]);
  const [image, setImage] = useState<string | null>(null);
  const [isCapturing, setIsCapturing] = useState(false); // Track whether capturing is active
  const webcamRef = React.useRef<Webcam>(null);

  // Capture function to get screenshot from webcam
  const capture = React.useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      setImage(imageSrc); // Save the captured image
      console.log("image captured")
    }
  }, [webcamRef]);

  // Function to toggle timer
  const toggleCapture = () => {
    setIsCapturing(prev => !prev);
  };

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
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
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
            <WebcamCapture />
            <div className="bg-white rounded-2xl p-4 shadow-lg">
              <h3 className="text-lg font-semibold mb-2">Current Emotion</h3>
              <p className="text-gray-600">Waiting for emotion detection...</p>
            </div>
          </div>
        </div>
      </div>
    </NextUIProvider>
=======
  const roastUser = async () => {
    if (!image) return;

    const response = await fetch('http://localhost:5000/roast', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image }),
    });

    const data = await response.json();
    setMessages(prev => [...prev, `Roast: ${data.roast}`]);
  };

  useEffect(() => {
    console.log('hi');
  }, []);

  return (
    <div style={{ display: 'flex', padding: '20px' }}>
      <Duck emotion={emotion} />
      <Spacer x={2} />
      <Card style={{ width: '300px', padding: '20px' }}>
        <Webcam
          ref={webcamRef}
          screenshotFormat="image/jpeg" // Ensure screenshots are captured as images
        />
        {image && (
          <div>
            <h4>Captured Image:</h4>
            <img src={image} alt="Captured" style={{ width: '100%', marginTop: '10px' }} />
          </div>
        )}

        <Chat messages={messages} />
        <Spacer y={1} />
        <Button onClick={analyzeImage}>Analyze Emotion</Button>
        <Spacer y={1} />
        <Button onClick={roastUser}>Roast Me</Button>
      </Card>
    </div>
>>>>>>> Stashed changes
  );
}

export default App;
