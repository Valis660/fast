import React from 'react';
import { Search, Calendar, MapPin, RotateCcw } from 'lucide-react';
import { HotelFilters as HotelFiltersType } from '../../api/types';

interface HotelFiltersProps {
  filters: HotelFiltersType;
  onFiltersChange: (filters: HotelFiltersType) => void;
  onSearch?: () => void;
}

const HotelFilters: React.FC<HotelFiltersProps> = ({ filters, onFiltersChange, onSearch }) => {
  const handleInputChange = (field: keyof HotelFiltersType, value: string) => {
    onFiltersChange({
      ...filters,
      [field]: value,
    });
  };

  const handleSearch = () => {
    if (onSearch) {
      onSearch();
    }
  };

  const handleReset = () => {
    onFiltersChange({
      date_from: new Date().toISOString().split('T')[0],
      date_to: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      page: 1,
      size: 20,
    });
  };

  return (
    <div className="card p-6 mb-8">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Поиск отелей</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Search className="w-4 h-4 inline mr-1" />
            Название отеля
          </label>
          <input
            type="text"
            className="input"
            placeholder="Введите название"
            value={filters.title || ''}
            onChange={(e) => handleInputChange('title', e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <MapPin className="w-4 h-4 inline mr-1" />
            Местоположение
          </label>
          <input
            type="text"
            className="input"
            placeholder="Введите город"
            value={filters.location || ''}
            onChange={(e) => handleInputChange('location', e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Calendar className="w-4 h-4 inline mr-1" />
            Дата заезда
          </label>
          <input
            type="date"
            className="input"
            value={filters.date_from}
            onChange={(e) => handleInputChange('date_from', e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Calendar className="w-4 h-4 inline mr-1" />
            Дата выезда
          </label>
          <input
            type="date"
            className="input"
            value={filters.date_to}
            onChange={(e) => handleInputChange('date_to', e.target.value)}
          />
        </div>
      </div>
      
      <div className="flex justify-end gap-3 mt-6">
        <button
          type="button"
          onClick={handleReset}
          className="btn btn-outline flex items-center gap-2"
        >
          <RotateCcw className="w-4 h-4" />
          Сбросить
        </button>
        <button
          type="button"
          onClick={handleSearch}
          className="btn btn-primary flex items-center gap-2"
        >
          <Search className="w-4 h-4" />
          Найти отели
        </button>
      </div>
    </div>
  );
};

export default HotelFilters;

