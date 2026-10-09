export type UserRole = 'SUPERADMIN' | 'WHOLESALER_ADMIN' | 'WHOLESALER_MANAGER' | 'RETAILER_ADMIN' | 'RETAILER_STAFF' | 'DRIVER'
export type OrgType = 'RETAILER' | 'WHOLESALER'
export type OrgStatus = 'PENDING' | 'ACTIVE' | 'SUSPENDED'
export type OrderStatus = 'PENDING' | 'CONFIRMED' | 'DISPATCHED' | 'DELIVERED' | 'PARTIALLY_RETURNED' | 'COMPLETED' | 'CANCELLED'
export type DeliveryType = 'SELF_PICKUP' | 'WHOLESALER_DELIVERY'
export type UnitType = 'PIECE' | 'KG' | 'LITRE' | 'BOX' | 'PACK'
export type TransactionType = 'DEBIT_FEE' | 'CREDIT_PAYMENT' | 'ADJUSTMENT'
export type ReturnActStatus = 'DRAFT' | 'SUBMITTED' | 'ACCEPTED' | 'DISPUTED'

export interface Organization { id: string; name: string; type: OrgType; legal_details: any; inn: string | null; status: OrgStatus; created_at: string; }
export interface Branch { id: string; organization_id: string; name: string; address: string | null; phone: string | null; is_active: boolean; }
export interface User { id: string; organization_id: string; branch_id: string | null; full_name: string; phone: string; role: UserRole; is_active: boolean; last_login: string | null; }
export interface Product { id: string; title: string; barcode: string | null; sku: string | null; category: string | null; subcategory: string | null; unit_type: UnitType; image_url: string | null; is_active: boolean; }
export interface WholesalerInventory { id: string; branch_id: string; global_product_id: string; price: number; moq: number; available_stock: number; reserved_stock: number; is_active: boolean; product?: Product; }
export interface Order { id: string; order_number: string; retailer_branch_id: string; wholesaler_branch_id: string; status: OrderStatus; delivery_type: DeliveryType; total_amount: number; platform_fee: number; final_amount: number; created_at: string; items?: OrderItem[]; retailer_branch?: Branch; wholesaler_branch?: Branch; }
export interface OrderItem { id: string; order_id: string; global_product_id: string; ordered_qty: number; delivered_qty: number; returned_qty: number; unit_price: number; line_total: number; product?: Product; }
export interface BillingEntry { id: string; organization_id: string; transaction_type: TransactionType; amount: number; balance_after: number; reference_order_id: string | null; description: string | null; created_at: string; }
export interface PaginatedResponse<T> { items: T[]; total: number; page: number; per_page: number; pages: number; }
