import React from 'react';
import { Card, Avatar } from "@nextui-org/react";
import { User } from 'lucide-react';
import Duck from './Duck';

interface ChatMessageProps {
  message: string;
  isAI: boolean;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message, isAI }) => {
  return (
    <div className={`flex gap-3 ${isAI ? '' : 'flex-row-reverse'}`}>
      <Avatar
        icon={isAI ? <Duck /> : <User />}
        classNames={{
          base: `${isAI ? 'bg-purple-600' : 'bg-blue-600'}`,
          icon: "text-white/90"
        }}
      />
      <Card className={`p-4 max-w-[80%] ${isAI ? 'bg-purple-100' : 'bg-blue-100'}`}>
        <p>{message}</p>
      </Card>
    </div>
  );
};