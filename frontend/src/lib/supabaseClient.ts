import { createClient } from '@supabase/supabase-js'

// These should be loaded from env vars but for now we might need to instruct user
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || ''
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || ''

if (!supabaseUrl || !supabaseAnonKey) {
    console.warn("Supabase credentials missing. Authentication will fail.")
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
