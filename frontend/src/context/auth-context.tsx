import React, { createContext, useContext, useState, useEffect } from "react";
import { supabase } from "../lib/supabase";
import type { UserType } from "../lib/schemas";
import {
  type AuthResponse,
  type AuthError,
  type User,
} from "@supabase/supabase-js";

type AuthProviderProps = {
  children: React.ReactNode;
};

type AuthContextType = {
  user: UserType | null;
  loading: boolean;
  signUp: (
    email: string,
    password: string,
    firstName: string,
    lastName: string
  ) => Promise<{ data: AuthResponse["data"]; error: AuthError | null }>;
  signIn: (
    email: string,
    password: string
  ) => Promise<{ data: AuthResponse["data"]; error: AuthError | null }>;
  signOut: () => Promise<{ error: AuthError | null }>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<UserType | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get initial session
    const getSession = async () => {
      const {
        data: { session },
      } = await supabase.auth.getSession();

      setUser(session?.user ? transformUser(session.user) : null);
      setLoading(false);
    };

    getSession();

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange(async (_, session) => {
      setUser(session?.user ? transformUser(session.user) : null);
      setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  // Helper function to transform Supabase user to your UserType
  const transformUser = (supabaseUser: User): UserType | null => {
    if (!supabaseUser?.email) return null;

    return {
      id: supabaseUser.id,
      email: supabaseUser.email,
      created_at: supabaseUser.created_at ?? "",
      updated_at: supabaseUser.updated_at ?? "",
    };
  };

  const signUp = async (
    email: string,
    password: string,
    firstName: string,
    lastName: string
  ) => {
    const response = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          firstName,
          lastName,
        },
      },
    });
    return { data: response.data, error: response.error };
  };

  const signIn = async (email: string, password: string) => {
    const response = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    return { data: response.data, error: response.error };
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    return { error };
  };

  const value = {
    user,
    loading,
    signUp,
    signIn,
    signOut,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
