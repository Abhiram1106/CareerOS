import { api, type AuthResponse } from "../../lib/api";

export type LoginPayload = { email: string; password: string };
export type RegisterPayload = {
  email: string;
  password: string;
  full_name: string;
};

export async function login(payload: LoginPayload): Promise<AuthResponse> {
  return api.login(payload);
}

export async function register(payload: RegisterPayload): Promise<AuthResponse> {
  return api.register(payload);
}
