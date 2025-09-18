import React from 'react';
import { Bed, Users, Wifi, Car, Coffee } from 'lucide-react';
import { Room } from '../../api/types';

interface RoomCardProps {
  room: Room;
  onBook: (room: Room) => void;
  isAuthenticated: boolean;
}

const RoomCard: React.FC<RoomCardProps> = ({ room, onBook, isAuthenticated }) => {
  const getServiceIcon = (serviceTitle: string) => {
    const title = serviceTitle.toLowerCase();
    if (title.includes('wifi') || title.includes('интернет')) return <Wifi className="w-4 h-4" />;
    if (title.includes('парковка') || title.includes('авто')) return <Car className="w-4 h-4" />;
    if (title.includes('завтрак') || title.includes('еда')) return <Coffee className="w-4 h-4" />;
    return <Bed className="w-4 h-4" />;
  };

  return (
    <div className="card p-6">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {room.title}
          </h3>
          {room.description && (
            <p className="text-gray-600 text-sm mb-3">
              {room.description}
            </p>
          )}
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-primary-600">
            {room.price.toLocaleString()} ₽
          </div>
          <div className="text-sm text-gray-500">за ночь</div>
        </div>
      </div>

      <div className="flex items-center text-gray-600 mb-4">
        <Users className="w-4 h-4 mr-1" />
        <span className="text-sm">До {room.quantity} гостей</span>
      </div>

      {room.uslugi.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Услуги:</h4>
          <div className="flex flex-wrap gap-2">
            {room.uslugi.map((service) => (
              <div
                key={service.id}
                className="flex items-center space-x-1 bg-gray-100 px-2 py-1 rounded-md text-xs"
              >
                {getServiceIcon(service.title)}
                <span>{service.title}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <button
        onClick={() => onBook(room)}
        disabled={!isAuthenticated}
        className={`w-full py-2 px-4 rounded-lg font-medium transition-colors ${
          isAuthenticated
            ? 'bg-primary-600 text-white hover:bg-primary-700'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
      >
        {isAuthenticated ? 'Забронировать' : 'Войдите для бронирования'}
      </button>
    </div>
  );
};

export default RoomCard;

