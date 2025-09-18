export interface User {
  id: number;
  email: string;
  name?: string;
}

export interface Hotel {
  id: number;
  title: string;
  location: string;
}

export interface Room {
  id: number;
  hotel_id: number;
  title: string;
  description?: string;
  price: number;
  quantity: number;
  uslugi: Service[];
}

export interface Service {
  id: number;
  title: string;
}

export interface Booking {
  id: number;
  user_id: number;
  room_id: number;
  date_from: string;
  date_to: string;
  price: number;
  total_coast: number;
  room?: Room;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name?: string;
}

export interface BookingRequest {
  room_id: number;
  date_from: string;
  date_to: string;
}

export interface HotelFilters {
  location?: string;
  title?: string;
  date_from: string;
  date_to: string;
  page?: number;
  size?: number;
}

