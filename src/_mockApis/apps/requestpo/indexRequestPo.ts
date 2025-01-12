import axios from 'axios';

export type KeyedObject = {
  [key: string]: string | number | null | undefined | KeyedObject | any;
};

const REQUEST_PO_API_URL = 'http://127.0.0.1:8000/requestpo/';

// Fetch all Purchase Orders (READ)
export const fetchRequestPOs = async (): Promise<KeyedObject[]> => {
  try {
    const response = await axios.get(REQUEST_PO_API_URL);
    return response.data.map((item: any) => ({
      id: item.poid || '',
      orderDate: item.orderdate || '',
      vendorData: item.vendordata || '',
      itemName: item.itemname || '',
      itemDesc: item.itemdesc || '',
      itemPrice: item.itemprice || '',
      itemQty: item.itemqty || '',
      paymentProof: item.paymentproof || '',
      submitNotes: item.submitnotes || '',
      adminId: item.adminid || '',
    }));
  } catch (error) {
    console.error('Error fetching purchase orders from API:', error);
    throw new Error('Failed to fetch purchase orders');
  }
};

// Add a new Purchase Order (INSERT)
export const addRequestPO = async (newRequestPO: KeyedObject): Promise<void> => {
  try {
    await axios.post(REQUEST_PO_API_URL, {
      orderdate: newRequestPO.orderDate,
      vendordata: newRequestPO.vendorData,
      itemname: newRequestPO.itemName,
      itemdesc: newRequestPO.itemDesc,
      itemprice: newRequestPO.itemPrice,
      itemqty: newRequestPO.itemQty,
      paymentproof: newRequestPO.paymentProof,
      submitnotes: newRequestPO.submitNotes,
      adminid: '01700551',
    });
  } catch (error) {
    console.error('Error adding purchase order:', error);
    throw new Error('Failed to add purchase order');
  }
};

// Delete a Purchase Order (DELETE)
export const deleteRequestPO = async (poId: string): Promise<void> => {
  try {
    await axios.delete(REQUEST_PO_API_URL, {
      data: {
        poid: poId,
        adminid: '01700551',
      },
    });
  } catch (error) {
    console.error('Error deleting purchase order:', error);
    throw new Error('Failed to delete purchase order');
  }
};
