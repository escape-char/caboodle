
export interface Permission{
  id: number;
  name: string;
  description: string;
  resource_id: number;
  created_at?: string;
  modified_at?: string;
}

export interface Role{
  id: number;
  name: string;
  description: string;
  resource_id: number;
  permissions: Array<Permission>;
  created_at?: string;
  modified_at?: string;
}

export interface User{
  id: number;
  username: string;
  email: string;
  name: string;
  dark_theme?: boolean;
  retries?: number;
  locked_until?: string;
  last_login?: string;
  roles: Array<Role>;
  created_at?: string;
  modified_at?: string;
}
