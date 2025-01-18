import React from 'react';

interface ChatProps {
  messages: string[];
}

const Chat = ({ messages }: ChatProps) => {
  return (
    <div style={{ height: '400px', overflowY: 'auto', border: '1px solid #ccc', padding: '10px' }}>
      {messages.map((message, index) => (
        <div key={index} style={{ marginBottom: '10px' }}>
          {message}
        </div>
      ))}
    </div>
  );
};

export default Chat;