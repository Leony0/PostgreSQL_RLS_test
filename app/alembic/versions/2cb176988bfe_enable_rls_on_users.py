"""enable RLS on users

Revision ID: 2cb176988bfe
Revises: 283f176864e9
Create Date: 2025-05-29 00:22:17.995945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cb176988bfe'
down_revision: Union[str, None] = '283f176864e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE users ENABLE ROW LEVEL SECURITY;")
    op.execute("""
        CREATE POLICY tenant_policy_users ON users
        FOR SELECT
        USING (tenant_id = current_setting('app.current_tenant_id')::int);
    """)
    op.execute("ALTER TABLE projects ENABLE ROW LEVEL SECURITY;")
    op.execute("""
        CREATE POLICY tenant_policy_projects ON projects
        FOR SELECT
        USING (
            (SELECT tenant_id FROM users WHERE users.id = projects.user_id)
            = current_setting('app.current_tenant_id')::int
        );
    """)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
