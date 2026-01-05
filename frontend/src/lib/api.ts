import { supabase } from './supabaseClient';

const API_URL = 'https://bsc360-app.onrender.com';

export const analyzeData = async (data: any) => {
    try {
        const session = await supabase.auth.getSession();
        const token = session.data.session?.access_token;

        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error analyzing data:', error);
        throw error;
    }
};

