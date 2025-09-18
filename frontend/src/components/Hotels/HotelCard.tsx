import React from 'react';
import { Link } from 'react-router-dom';
import { MapPin, Star } from 'lucide-react';
import { Hotel } from '../../api/types';

interface HotelCardProps {
  hotel: Hotel;
}

const HotelCard: React.FC<HotelCardProps> = ({ hotel }) => {
  return (
    <Link to={`/hotels/${hotel.id}`} className="block">
      <div className="card-hover p-6 h-full">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {hotel.title}
            </h3>
            <div className="flex items-center text-gray-600 mb-3">
              <MapPin className="w-4 h-4 mr-1" />
              <span className="text-sm">{hotel.location}</span>
            </div>
          </div>
          <div className="flex items-center">
            <Star className="w-4 h-4 text-yellow-400 fill-current" />
            <span className="ml-1 text-sm text-gray-600">4.5</span>
          </div>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Посмотреть номера</span>
          <div className="w-6 h-6 bg-primary-100 rounded-full flex items-center justify-center">
            <svg className="w-3 h-3 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default HotelCard;

