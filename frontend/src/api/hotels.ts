import { apiClient } from './client';
import { Hotel, HotelFilters, Room } from './types';

export const hotelsApi = {
  getHotels: async (filters: HotelFilters): Promise<{ data: Hotel[]; total: number }> => {
    const params = new URLSearchParams();
    
    if (filters.location) params.append('location', filters.location);
    if (filters.title) params.append('title', filters.title);
    params.append('date_from', filters.date_from);
    params.append('date_to', filters.date_to);
    if (filters.page) params.append('page', filters.page.toString());
    if (filters.size) params.append('size', filters.size.toString());

    const response = await apiClient.get(`/hotels?${params.toString()}`);
    // API возвращает массив отелей, оборачиваем в объект с data и total
    const hotels = Array.isArray(response.data) ? response.data : [];
    return {
      data: hotels,
      total: hotels.length
    };
  },

  getHotel: async (id: number): Promise<Hotel> => {
    const response = await apiClient.get(`/hotels/${id}`);
    return response.data;
  },

  getHotelRooms: async (hotelId: number, dateFrom?: string, dateTo?: string): Promise<Room[]> => {
    const params = new URLSearchParams();
    if (dateFrom) params.append('date_from', dateFrom);
    if (dateTo) params.append('date_to', dateTo);
    
    const response = await apiClient.get(`/hotels/${hotelId}/rooms/?${params.toString()}`);
    return response.data;
  },
};

