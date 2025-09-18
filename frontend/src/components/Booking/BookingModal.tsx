import React, { useState } from 'react';
import { X, Calendar, CreditCard } from 'lucide-react';
import { Room } from '../../api/types';
import { useAuth } from '../../contexts/AuthContext';
import { bookingsApi } from '../../api/bookings';
import toast from 'react-hot-toast';

interface BookingModalProps {
  room: Room | null;
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

const BookingModal: React.FC<BookingModalProps> = ({ room, isOpen, onClose, onSuccess }) => {
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { isAuthenticated } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!room || !isAuthenticated) return;

    if (!dateFrom || !dateTo) {
      toast.error('Выберите даты заезда и выезда');
      return;
    }

    if (new Date(dateFrom) >= new Date(dateTo)) {
      toast.error('Дата выезда должна быть позже даты заезда');
      return;
    }

    setIsLoading(true);

    try {
      await bookingsApi.createBooking({
        room_id: room.id,
        date_from: dateFrom,
        date_to: dateTo,
      });

      toast.success('Бронирование успешно создано!');
      onSuccess();
      onClose();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Ошибка создания бронирования');
    } finally {
      setIsLoading(false);
    }
  };

  const calculateTotal = () => {
    if (!dateFrom || !dateTo || !room) return 0;
    
    const startDate = new Date(dateFrom);
    const endDate = new Date(dateTo);
    const nights = Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));
    
    return nights * room.price;
  };

  if (!isOpen || !room) return null;

  const totalNights = dateFrom && dateTo 
    ? Math.ceil((new Date(dateTo).getTime() - new Date(dateFrom).getTime()) / (1000 * 60 * 60 * 24))
    : 0;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Бронирование номера</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          <div className="mb-6">
            <h3 className="font-medium text-gray-900 mb-2">{room.title}</h3>
            <div className="text-2xl font-bold text-primary-600">
              {room.price.toLocaleString()} ₽ <span className="text-sm font-normal text-gray-500">за ночь</span>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="w-4 h-4 inline mr-1" />
                Дата заезда
              </label>
              <input
                type="date"
                required
                className="input"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                min={new Date().toISOString().split('T')[0]}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="w-4 h-4 inline mr-1" />
                Дата выезда
              </label>
              <input
                type="date"
                required
                className="input"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                min={dateFrom || new Date().toISOString().split('T')[0]}
              />
            </div>

            {totalNights > 0 && (
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="flex justify-between text-sm mb-2">
                  <span>Количество ночей:</span>
                  <span>{totalNights}</span>
                </div>
                <div className="flex justify-between text-sm mb-2">
                  <span>Цена за ночь:</span>
                  <span>{room.price.toLocaleString()} ₽</span>
                </div>
                <div className="border-t pt-2 flex justify-between font-semibold">
                  <span>Итого:</span>
                  <span className="text-primary-600">{calculateTotal().toLocaleString()} ₽</span>
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading || !isAuthenticated}
              className="w-full btn btn-primary flex items-center justify-center space-x-2"
            >
              <CreditCard className="w-4 h-4" />
              <span>{isLoading ? 'Бронирование...' : 'Забронировать'}</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default BookingModal;

