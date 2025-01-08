import axios from 'axios';

export type KeyedObject = {
    [key: string]: string | number | null | undefined | KeyedObject | any;
};

const API_URL = 'http://127.0.0.1:8000/locklimitrekening/';

export const fetchLockRekeningStatus = async (): Promise<KeyedObject> => {
    try {
        const response = await axios.get(API_URL);
        return {
            id: response.data.rek_id || '',     // Rekening ID
            isActive: response.data.lock_rek === '1', // Status lock (true jika "1")
        };
    } catch (error) {
        console.error('Error fetching lock rekening status from API:', error);
        throw new Error('Failed to fetch lock rekening status');
    }
};

export const updateLockRekeningStatus = async (isActive: boolean): Promise<void> => {
    try {
        await axios.put(API_URL, {
            lock_rek: isActive ? '1' : '0', // "1" untuk lock, "0" untuk unlock
            add_user: '01700551',          // User yang melakukan operasi
        });
    } catch (error) {
        console.error('Error updating lock rekening status:', error);
        throw new Error('Failed to update lock rekening status');
    }
};
