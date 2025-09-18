import { apiClient } from './client';
import { Booking, BookingRequest } from './types';

export const bookingsApi = {
  getBookings: async (): Promise<Booking[]> => {
    const response = await apiClient.get('/bookings');
    return response.data;
  },

  getMyBookings: async (): Promise<Booking[]> => {
    const response = await apiClient.get('/bookings/me');
    return response.data;
  },

  createBooking: async (data: BookingRequest): Promise<Booking> => {
    const response = await apiClient.post('/bookings', data);
    return response.data.data;
  },
};

