import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { MapPin, Star, ArrowLeft } from 'lucide-react';
import { hotelsApi } from '../api/hotels';
import { Room } from '../api/types';
import { useAuth } from '../contexts/AuthContext';
import RoomCard from '../components/Booking/RoomCard';
import BookingModal from '../components/Booking/BookingModal';
import { Loader2 } from 'lucide-react';

const HotelDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [selectedRoom, setSelectedRoom] = useState<Room | null>(null);
  const [isBookingModalOpen, setIsBookingModalOpen] = useState(false);

  const { data: hotel, isLoading: hotelLoading } = useQuery(
    ['hotel', id],
    () => hotelsApi.getHotel(Number(id)),
    {
      enabled: !!id,
    }
  );

  const { data: rooms, isLoading: roomsLoading } = useQuery(
    ['rooms', id],
    () => hotelsApi.getHotelRooms(Number(id), '2025-09-13', '2025-09-20'),
    {
      enabled: !!id,
    }
  );

  const handleBookRoom = (room: Room) => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    setSelectedRoom(room);
    setIsBookingModalOpen(true);
  };

  const handleBookingSuccess = () => {
    // Можно добавить обновление данных или другие действия
  };

  if (hotelLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
        <span className="ml-2 text-gray-600">Загрузка отеля...</span>
      </div>
    );
  }

  if (!hotel) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Отель не найден</p>
        <button
          onClick={() => navigate('/')}
          className="mt-4 btn btn-primary"
        >
          Вернуться к списку отелей
        </button>
      </div>
    );
  }

  return (
    <div>
      <button
        onClick={() => navigate('/')}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Назад к отелям</span>
      </button>

      <div className="card p-8 mb-8">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {hotel.title}
            </h1>
            <div className="flex items-center text-gray-600 mb-4">
              <MapPin className="w-5 h-5 mr-2" />
              <span>{hotel.location}</span>
            </div>
            <div className="flex items-center">
              <Star className="w-5 h-5 text-yellow-400 fill-current mr-1" />
              <span className="text-lg font-semibold">4.5</span>
              <span className="text-gray-500 ml-2">(128 отзывов)</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-200 rounded-lg h-64 flex items-center justify-center">
            <span className="text-gray-500">Фото отеля</span>
          </div>
          <div className="bg-gray-200 rounded-lg h-64 flex items-center justify-center">
            <span className="text-gray-500">Дополнительные фото</span>
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Описание</h2>
          <p className="text-gray-600 leading-relaxed">
            Прекрасный отель с современными удобствами и отличным сервисом. 
            Идеально подходит для деловых поездок и отдыха. 
            Расположен в удобном месте с легким доступом к основным достопримечательностям.
          </p>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">Доступные номера</h2>
        
        {roomsLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
            <span className="ml-2 text-gray-600">Загрузка номеров...</span>
          </div>
        ) : rooms && rooms.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {rooms.map((room) => (
              <RoomCard
                key={room.id}
                room={room}
                onBook={handleBookRoom}
                isAuthenticated={isAuthenticated}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-600">Номера не найдены</p>
          </div>
        )}
      </div>

      <BookingModal
        room={selectedRoom}
        isOpen={isBookingModalOpen}
        onClose={() => {
          setIsBookingModalOpen(false);
          setSelectedRoom(null);
        }}
        onSuccess={handleBookingSuccess}
      />
    </div>
  );
};

export default HotelDetailPage;

