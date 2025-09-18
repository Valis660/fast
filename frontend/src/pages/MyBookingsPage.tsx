import React from 'react';
import { useQuery } from 'react-query';
import { Calendar, MapPin, CreditCard, Clock } from 'lucide-react';
import { bookingsApi } from '../api/bookings';
import { format, parseISO } from 'date-fns';
import { Loader2 } from 'lucide-react';

const MyBookingsPage: React.FC = () => {
  const { data: bookings, isLoading, error } = useQuery(
    'myBookings',
    () => bookingsApi.getMyBookings(),
    {
      retry: 1,
    }
  );

  // Отладочная информация
  console.log('MyBookingsPage - isLoading:', isLoading);
  console.log('MyBookingsPage - error:', error);
  console.log('MyBookingsPage - bookings:', bookings);
  if (bookings && bookings.length > 0) {
    console.log('MyBookingsPage - first booking:', bookings[0]);
    console.log('MyBookingsPage - first booking total_coast:', bookings[0].total_coast);
    console.log('MyBookingsPage - first booking price:', bookings[0].price);
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
        <span className="ml-2 text-gray-600">Загрузка бронирований...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">Ошибка загрузки бронирований</p>
      </div>
    );
  }

  if (!bookings || bookings.length === 0) {
    return (
      <div className="text-center py-12">
        <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">
          У вас пока нет бронирований
        </h2>
        <p className="text-gray-600 mb-6">
          Найдите подходящий отель и создайте свое первое бронирование
        </p>
        <a
          href="/"
          className="btn btn-primary"
        >
          Найти отели
        </a>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Мои бронирования
        </h1>
        <p className="text-gray-600">
          Управляйте своими бронированиями и отслеживайте статус
        </p>
      </div>

      <div className="space-y-6">
        {bookings.map((booking) => (
          <div key={booking.id} className="card p-6">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
              <div className="flex-1 mb-4 lg:mb-0">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {booking.room?.title || 'Номер'}
                </h3>
                
                {booking.room && (
                  <div className="flex items-center text-gray-600 mb-2">
                    <MapPin className="w-4 h-4 mr-1" />
                    <span className="text-sm">Отель ID: {booking.room.hotel_id}</span>
                  </div>
                )}

                <div className="flex items-center space-x-6 text-sm text-gray-600">
                  <div className="flex items-center">
                    <Calendar className="w-4 h-4 mr-1" />
                    <span>
                      {format(parseISO(booking.date_from), 'dd MMM yyyy')} - {' '}
                      {format(parseISO(booking.date_to), 'dd MMM yyyy')}
                    </span>
                  </div>
                  
                  <div className="flex items-center">
                    <Clock className="w-4 h-4 mr-1" />
                    <span>
                      {Math.ceil(
                        (new Date(booking.date_to).getTime() - new Date(booking.date_from).getTime()) / 
                        (1000 * 60 * 60 * 24)
                      )} ночей
                    </span>
                  </div>
                </div>
              </div>

              <div className="flex flex-col lg:items-end">
                <div className="text-right mb-2">
                  <div className="text-2xl font-bold text-primary-600">
                    {booking.total_coast?.toLocaleString() || '0'} ₽
                  </div>
                  <div className="text-sm text-gray-500">
                    {booking.price?.toLocaleString() || '0'} ₽ за ночь
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <div className="flex items-center bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                    <CreditCard className="w-3 h-3 mr-1" />
                    Подтверждено
                  </div>
                </div>
              </div>
            </div>

            {booking.room?.uslugi && booking.room.uslugi.length > 0 && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Включенные услуги:</h4>
                <div className="flex flex-wrap gap-2">
                  {booking.room.uslugi.map((service) => (
                    <span
                      key={service.id}
                      className="bg-gray-100 text-gray-700 px-2 py-1 rounded-md text-xs"
                    >
                      {service.title}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default MyBookingsPage;
