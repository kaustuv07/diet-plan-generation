"""Initial migration.

Revision ID: 9a8d8e95d2db
Revises: 6440dca24971
Create Date: 2024-08-23 12:02:05.023848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a8d8e95d2db'
down_revision = '6440dca24971'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('diet_plan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=150), nullable=False),
    sa.Column('diet_plan', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('food',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('caloric_value', sa.Float(), nullable=False),
    sa.Column('fat', sa.Float(), nullable=False),
    sa.Column('saturated_fats', sa.Float(), nullable=False),
    sa.Column('monounsaturated_fats', sa.Float(), nullable=False),
    sa.Column('polyunsaturated_fats', sa.Float(), nullable=False),
    sa.Column('carbohydrates', sa.Float(), nullable=False),
    sa.Column('sugars', sa.Float(), nullable=False),
    sa.Column('protein', sa.Float(), nullable=False),
    sa.Column('dietary_fiber', sa.Float(), nullable=False),
    sa.Column('cholesterol', sa.Float(), nullable=False),
    sa.Column('sodium', sa.Float(), nullable=False),
    sa.Column('water', sa.Float(), nullable=False),
    sa.Column('vitamin_a', sa.Float(), nullable=False),
    sa.Column('vitamin_b1', sa.Float(), nullable=False),
    sa.Column('vitamin_b11', sa.Float(), nullable=False),
    sa.Column('vitamin_b12', sa.Float(), nullable=False),
    sa.Column('vitamin_b2', sa.Float(), nullable=False),
    sa.Column('vitamin_b3', sa.Float(), nullable=False),
    sa.Column('vitamin_b5', sa.Float(), nullable=False),
    sa.Column('vitamin_b6', sa.Float(), nullable=False),
    sa.Column('vitamin_c', sa.Float(), nullable=False),
    sa.Column('vitamin_d', sa.Float(), nullable=False),
    sa.Column('vitamin_e', sa.Float(), nullable=False),
    sa.Column('vitamin_k', sa.Float(), nullable=False),
    sa.Column('calcium', sa.Float(), nullable=False),
    sa.Column('copper', sa.Float(), nullable=False),
    sa.Column('iron', sa.Float(), nullable=False),
    sa.Column('magnesium', sa.Float(), nullable=False),
    sa.Column('manganese', sa.Float(), nullable=False),
    sa.Column('phosphorus', sa.Float(), nullable=False),
    sa.Column('potassium', sa.Float(), nullable=False),
    sa.Column('selenium', sa.Float(), nullable=False),
    sa.Column('zinc', sa.Float(), nullable=False),
    sa.Column('nutrition_density', sa.Float(), nullable=False),
    sa.Column('meal_type', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('goal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('calories', sa.Integer(), nullable=False),
    sa.Column('protein', sa.Integer(), nullable=False),
    sa.Column('carbs', sa.Integer(), nullable=False),
    sa.Column('fat', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('goal')
    op.drop_table('user')
    op.drop_table('food')
    op.drop_table('diet_plan')
    # ### end Alembic commands ###
