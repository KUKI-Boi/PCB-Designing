/**
 * API client for AI Hardware Designer
 */
const API_BASE_URL = 'http://localhost:8000';

export const generateHardware = async (prompt) => {
    try {
        const response = await fetch(`${API_BASE_URL}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate hardware');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
};

export const getDownloadUrl = (path) => `${API_BASE_URL}${path}`;
