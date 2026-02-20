from sqlalchemy import create_engine,String, ForeignKey
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship



class Base(DeclarativeBase):
    pass

class CashCount_Model(Base):
    __tablename__ = "cashcount"
    id:Mapped[int] = mapped_column(primary_key=True)
    category:Mapped[str] = mapped_column(String(20),default="")
    tag:Mapped[str] = mapped_column(String(20),default="")
    value:Mapped[str] = mapped_column(String(20),default="")
    product:Mapped[str] = mapped_column(String(20),default="")

class AtdTables_Model(Base):
    __tablename__ = "atdTables"
    id:Mapped[int] = mapped_column(primary_key=True)
    category:Mapped[str] = mapped_column(String(20),default="")
    tag:Mapped[str] = mapped_column(String(20),default="")
    value:Mapped[str] = mapped_column(String(20),default="")

class Settings_Model(Base):
    __tablename__ = 'settings'
    id:Mapped[int] = mapped_column(primary_key=True)
    category:Mapped[str] = mapped_column(String(20),default="")
    tag:Mapped[str] = mapped_column(String(20),default="")
    value:Mapped[str] = mapped_column(String(200),default="")

class Personal(Base):
    __tablename__ = "personal"
    id:Mapped[int] = mapped_column(primary_key=True)
    branch:Mapped[str] = mapped_column(String(20),default="")
    date:Mapped[str] = mapped_column(String(20),default="")
    job_order:Mapped[str] = mapped_column(String(20),default="")
    reference:Mapped[str] = mapped_column(String(20),default="")
    dr_number:Mapped[str] = mapped_column(String(20),default="")
    warranty_start:Mapped[str] = mapped_column(String(20),default="")
    warranty_end:Mapped[str] = mapped_column(String(20),default="")
    remaining:Mapped[str] = mapped_column(String(20),default="")
    contact_number:Mapped[str] = mapped_column(String(20),default="")
    customer_name:Mapped[str] = mapped_column(String(40),default="")
    tech_name:Mapped[str] = mapped_column(String(40),default="")
    items:Mapped[list["Item"]] = relationship(back_populates='personal')
    def __str__(self):
        return f'{self.customer_name}_{self.dr_number}'
    
class Item(Base):
    __tablename__ = "item"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(20),default="")
    description:Mapped[str] = mapped_column(String(20),default="")
    serial:Mapped[str] = mapped_column(String(20),default="")
    customer_issues:Mapped[str] = mapped_column(String(100),default="")
    tech_finding:Mapped[str] = mapped_column(String(100),default="")

    personal_id:Mapped[int] = mapped_column(ForeignKey('personal.id'))
    personal:Mapped["Personal"] = relationship(back_populates='items')

    def __str__(self):
        return f'{self.name}_{self.personal_id}'

class QoutationItem(Base):
    __tablename__ = 'quote_items'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(200),default="")
    description:Mapped[str] = mapped_column(String(300),default="")
    t_qty:Mapped[str] = mapped_column(String(20),default="")
    retail_price:Mapped[str] = mapped_column(String(20),default="")
    price_four:Mapped[str] = mapped_column(String(20),default="")

    def __str__(self):
        return f'{self.description}'

