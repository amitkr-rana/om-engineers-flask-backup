from database import db
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

class Service(db.Model):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    duration: Mapped[str] = mapped_column(String(50), nullable=False)
    price_range: Mapped[str] = mapped_column(String(100), nullable=False)
    icon: Mapped[str] = mapped_column(String(10), nullable=False, default='🔧')
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with appointments
    appointments = db.relationship('Appointment', back_populates='service', cascade='all, delete-orphan')

    def to_dict(self) -> dict:
        """Convert service to dictionary representation"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'duration': self.duration,
            'price_range': self.price_range,
            'icon': self.icon,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def get_all(cls, active_only: bool = True):
        """Get all services"""
        query = cls.query
        if active_only:
            query = query.filter(cls.is_active == True)
        return query.all()

    @classmethod
    def get_by_category(cls, category: str, active_only: bool = True):
        """Get services by category"""
        query = cls.query.filter(cls.category == category)
        if active_only:
            query = query.filter(cls.is_active == True)
        return query.all()

    @classmethod
    def search(cls, query_str: str, active_only: bool = True):
        """Search services by name, description, or category"""
        query = cls.query.filter(
            db.or_(
                cls.name.ilike(f'%{query_str}%'),
                cls.description.ilike(f'%{query_str}%'),
                cls.category.ilike(f'%{query_str}%')
            )
        )
        if active_only:
            query = query.filter(cls.is_active == True)
        return query.all()

    @classmethod
    def get_categories(cls, active_only: bool = True):
        """Get all unique service categories"""
        query = db.session.query(cls.category).distinct()
        if active_only:
            query = query.filter(cls.is_active == True)
        return [cat[0] for cat in query.all()]

    @classmethod
    def initialize_default_services(cls):
        """Initialize default services if none exist"""
        if cls.query.count() > 0:
            return

        default_services = [
            {
                'name': 'Electrical Repair',
                'description': 'Complete electrical solutions for your home including wiring, outlets, and fixtures',
                'category': 'Electrical',
                'duration': '2-4 hours',
                'price_range': '₹500 - ₹2000',
                'icon': '⚡'
            },
            {
                'name': 'Plumbing Services',
                'description': 'Professional plumbing repairs and installations for all your water-related needs',
                'category': 'Plumbing',
                'duration': '1-3 hours',
                'price_range': '₹300 - ₹1500',
                'icon': '🔧'
            },
            {
                'name': 'AC Repair & Service',
                'description': 'Air conditioning repair, maintenance, and installation services',
                'category': 'HVAC',
                'duration': '1-2 hours',
                'price_range': '₹800 - ₹3000',
                'icon': '❄️'
            },
            {
                'name': 'Home Appliance Repair',
                'description': 'Repair services for washing machines, refrigerators, microwaves, and more',
                'category': 'Appliances',
                'duration': '2-3 hours',
                'price_range': '₹600 - ₹2500',
                'icon': '🏠'
            },
            {
                'name': 'Carpentry Services',
                'description': 'Furniture repair, custom woodwork, and carpentry solutions',
                'category': 'Carpentry',
                'duration': '3-6 hours',
                'price_range': '₹1000 - ₹5000',
                'icon': '🔨'
            },
            {
                'name': 'Painting Services',
                'description': 'Interior and exterior painting services for homes and offices',
                'category': 'Painting',
                'duration': '4-8 hours',
                'price_range': '₹1500 - ₹8000',
                'icon': '🎨'
            },
            {
                'name': 'Cleaning Services',
                'description': 'Deep cleaning, regular maintenance, and specialized cleaning services',
                'category': 'Cleaning',
                'duration': '2-4 hours',
                'price_range': '₹800 - ₹3000',
                'icon': '🧹'
            },
            {
                'name': 'Pest Control',
                'description': 'Safe and effective pest control solutions for your home',
                'category': 'Pest Control',
                'duration': '1-2 hours',
                'price_range': '₹1000 - ₹4000',
                'icon': '🐛'
            }
        ]

        for service_data in default_services:
            service = cls(**service_data)
            db.session.add(service)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def __str__(self) -> str:
        return f"Service(id={self.id}, name='{self.name}', category='{self.category}')"

    def __repr__(self) -> str:
        return self.__str__()