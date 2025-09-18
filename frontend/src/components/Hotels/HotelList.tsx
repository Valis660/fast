import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';
import { hotelsApi } from '../../api/hotels';
import { HotelFilters as HotelFiltersType } from '../../api/types';
import HotelCard from './HotelCard';
import HotelFilters from './HotelFilters';
import { Loader2 } from 'lucide-react';

interface HotelListProps {
  filters: HotelFiltersType;
  onFiltersChange: (filters: HotelFiltersType) => void;
}

const HotelList: React.FC<HotelListProps> = ({ filters, onFiltersChange }) => {
  const [searchTrigger, setSearchTrigger] = useState(0);
  
  const { data, isLoading, error } = useQuery(
    ['hotels', filters, searchTrigger],
    () => hotelsApi.getHotels(filters),
    {
      keepPreviousData: true,
    }
  );

  const handleSearch = () => {
    setSearchTrigger(prev => prev + 1);
  };

  // Автоматический поиск при изменении фильтров
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      setSearchTrigger(prev => prev + 1);
    }, 500); // Задержка 500мс для избежания слишком частых запросов

    return () => clearTimeout(timeoutId);
  }, [filters]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
        <span className="ml-2 text-gray-600">Загрузка отелей...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">Ошибка загрузки отелей</p>
      </div>
    );
  }

  const hotels = data?.data || [];

  return (
    <div>
      <HotelFilters 
        filters={filters} 
        onFiltersChange={onFiltersChange}
        onSearch={handleSearch}
      />
      
      {hotels.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-600">Отели не найдены</p>
          <p className="text-sm text-gray-500 mt-1">
            Попробуйте изменить параметры поиска
          </p>
        </div>
      ) : (
        <>
          <div className="mb-6">
            <p className="text-gray-600">
              Найдено отелей: <span className="font-semibold">{data?.total || 0}</span>
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {hotels.map((hotel) => (
              <HotelCard key={hotel.id} hotel={hotel} />
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default HotelList;

