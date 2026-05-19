"""adding common stock

Revision ID: 9b0eecfb12d1
Revises: d5ea64bf9045
Create Date: 2026-05-19 17:17:02.875850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b0eecfb12d1'
down_revision: Union[str, Sequence[str], None] = 'd5ea64bf9045'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('stock_common',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('object_type', sa.String(length=20), nullable=False),
    sa.Column('object_specs', sa.String(length=100), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    )    
    op.execute("""
        INSERT INTO stock_common (id, title, object_type, object_specs, quantity)
        VALUES
			(1, 'Magic Keyboard - US English, Bluetooth', 'keyboard', 'QWERTY Wireless APPLE', 1),
            (2, 'Magic Keyboard with Touch ID and Numeric Keypad for Mac Models with Apple Silicon - US English - Black Keys', 'keyboard', 'QWERTY Wireless NUMERIC_KEYPAD APPLE', 1),
            (3, 'K120 Wired Keyboard for Windows, USB Plug-and-Play, Full-Size, Spill-Resistant, Curved Space Bar, Compatible with PC, Laptop - Black', 'keyboard', 'QWERTY Wired LOGITECH', 1),
            (4, 'Magic Mouse - White Multi-Touch Surface', 'mouse', 'Wireless Bluetooth', 1),
            (5, 'Optical Mouse MS116 (275-BBCB)', 'mouse', 'Wired Logitech', 1)
    """)
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('stock_common')
    pass
    # ### end Alembic commands ###
