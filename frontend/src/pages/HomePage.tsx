import React, { useState } from 'react';
import { HotelFilters as HotelFiltersType } from '../api/types';
import HotelList from '../components/Hotels/HotelList';

const HomePage: React.FC = () => {
  const [filters, setFilters] = useState<HotelFiltersType>({
    date_from: new Date().toISOString().split('T')[0],
    date_to: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    page: 1,
    size: 20,
  });

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Найдите идеальный отель
        </h1>
        <p className="text-gray-600">
          Откройте для себя лучшие отели по всему миру и забронируйте незабываемое путешествие
        </p>
      </div>

      <HotelList filters={filters} onFiltersChange={setFilters} />
    </div>
  );
};

export default HomePage;

