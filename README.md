# PostgreSQL_RLS_test

これ手動実行する
-- この設定がないと SET app.current_tenant_id が無視されます

ALTER DATABASE rls_demo SET app.current_tenant_id TO '0';
