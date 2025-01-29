import axios from 'axios';

export type KeyedObject = {
    [key: string]: string | number | null | undefined | KeyedObject | any;
};

const API_URL = 'http://127.0.0.1:8000/summary_po_so/';

export const fetchSummaryPOSO = async (): Promise<KeyedObject[]> => {
    try {
        const response = await axios.get(API_URL); // Panggil endpoint untuk fetch data summary_po_so
        return response.data.map((item: any) => ({
            po_so_id: item.PoSo_ID || '', // PO/SO ID
            order_date: item.OrderDate || '', // Tanggal Pemesanan
            item_name: item.ItemName || '', // Nama Item
            item_price: item.ItemPrice || '', // Harga Item
            item_qty: item.ItemQty || '', // Jumlah Item
            total_item_price: item.TotalItemPrice || '', // Total Harga Item
            payment_status: item.PaymentStatus || '', // Status Pembayaran
            rekening_balance: item.ReckBalance || '', // Saldo Rekening
            add_user: item.AddUser || '', // Pengguna yang menambahkan
        }));
    } catch (error) {
        console.error('Error fetching summary PO & SO data:', error);
        throw new Error('Failed to fetch summary PO & SO data');
    }
};