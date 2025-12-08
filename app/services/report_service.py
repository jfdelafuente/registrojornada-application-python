"""Report service for advanced report generation and statistics."""

import json
from datetime import date, datetime, timedelta
from typing import List, Dict, Any
import logging

from app.models.workday import WorkdayRegistration, WeeklyReport
from app.models.enums import WorkdayTypeEnum
from app.config import get_settings

logger = logging.getLogger(__name__)


class ReportService:
    """
    Service for generating advanced reports and statistics.

    Features:
    - Weekly, monthly, and custom period reports
    - Statistical analysis (averages, totals, patterns)
    - Export to JSON format
    - Formatted output for Telegram
    """

    def __init__(self):
        """Initialize report service with settings."""
        self.settings = get_settings()

    def generate_weekly_summary(self, report: WeeklyReport) -> Dict[str, Any]:
        """
        Generate detailed weekly summary with statistics.

        Args:
            report: WeeklyReport object

        Returns:
            Dictionary with summary statistics
        """
        summary = {
            'period': {
                'start': report.start_date.strftime('%d/%m/%Y'),
                'end': report.end_date.strftime('%d/%m/%Y'),
                'days_in_period': (report.end_date - report.start_date).days + 1
            },
            'totals': {
                'days_worked': report.total_days,
                'telework_days': report.telework_days,
                'office_days': report.office_days,
                'total_hours': round(report.total_hours, 2)
            },
            'averages': {},
            'details': []
        }

        # Calculate averages
        if report.total_days > 0:
            summary['averages'] = {
                'hours_per_day': round(report.total_hours / report.total_days, 2),
                'telework_percentage': round((report.telework_days / report.total_days) * 100, 1),
                'office_percentage': round((report.office_days / report.total_days) * 100, 1)
            }
        else:
            summary['averages'] = {
                'hours_per_day': 0.0,
                'telework_percentage': 0.0,
                'office_percentage': 0.0
            }

        # Add daily details
        for reg in sorted(report.registrations, key=lambda x: x.date):
            summary['details'].append({
                'date': reg.date.strftime('%d/%m/%Y'),
                'day_of_week': self._get_day_name(reg.date.weekday()),
                'type': reg.workday_type.value,
                'location': reg.location or '',
                'start_time': reg.start_time,
                'end_time': reg.end_time,
                'hours': reg.calculate_hours()
            })

        return summary

    def calculate_statistics(
        self,
        registrations: List[WorkdayRegistration]
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics from registrations.

        Args:
            registrations: List of WorkdayRegistration objects

        Returns:
            Dictionary with statistical data
        """
        if not registrations:
            return self._empty_statistics()

        stats = {
            'total_registrations': len(registrations),
            'total_hours': 0.0,
            'total_days': len(set(reg.date for reg in registrations)),
            'by_type': {},
            'by_location': {},
            'by_day_of_week': {},
            'time_patterns': {}
        }

        # Initialize counters
        type_counts = {wt.value: 0 for wt in WorkdayTypeEnum}
        type_hours = {wt.value: 0.0 for wt in WorkdayTypeEnum}
        location_counts = {}
        day_counts = {i: 0 for i in range(7)}  # Monday=0, Sunday=6
        earliest_start = None
        latest_end = None

        # Process each registration
        for reg in registrations:
            hours = reg.calculate_hours()
            stats['total_hours'] += hours

            # By type
            type_counts[reg.workday_type.value] += 1
            type_hours[reg.workday_type.value] += hours

            # By location
            loc = reg.location or 'Unknown'
            location_counts[loc] = location_counts.get(loc, 0) + 1

            # By day of week
            day_counts[reg.date.weekday()] += 1

            # Time patterns
            if earliest_start is None or reg.start_time < earliest_start:
                earliest_start = reg.start_time
            if latest_end is None or reg.end_time > latest_end:
                latest_end = reg.end_time

        # Compile statistics
        stats['by_type'] = {
            wt: {
                'count': type_counts[wt],
                'hours': round(type_hours[wt], 2),
                'percentage': round((type_counts[wt] / len(registrations)) * 100, 1) if registrations else 0
            }
            for wt in type_counts
        }

        stats['by_location'] = {
            loc: {
                'count': count,
                'percentage': round((count / len(registrations)) * 100, 1)
            }
            for loc, count in location_counts.items()
        }

        stats['by_day_of_week'] = {
            self._get_day_name(day): count
            for day, count in day_counts.items()
        }

        stats['time_patterns'] = {
            'earliest_start': earliest_start,
            'latest_end': latest_end,
            'average_hours_per_day': round(stats['total_hours'] / stats['total_days'], 2) if stats['total_days'] > 0 else 0
        }

        stats['total_hours'] = round(stats['total_hours'], 2)

        return stats

    def export_to_json(
        self,
        report: WeeklyReport,
        include_statistics: bool = True
    ) -> str:
        """
        Export report to JSON format.

        Args:
            report: WeeklyReport to export
            include_statistics: If True, include statistical analysis

        Returns:
            JSON string
        """
        export_data = {
            'report_type': 'weekly',
            'generated_at': datetime.now().isoformat(),
            'period': {
                'start_date': report.start_date.isoformat(),
                'end_date': report.end_date.isoformat()
            },
            'summary': {
                'total_days': report.total_days,
                'telework_days': report.telework_days,
                'office_days': report.office_days,
                'total_hours': report.total_hours
            },
            'registrations': [
                {
                    'date': reg.date.isoformat(),
                    'start_time': reg.start_time,
                    'end_time': reg.end_time,
                    'workday_type': reg.workday_type.value,
                    'location': reg.location,
                    'hours_worked': reg.calculate_hours(),
                    'success': reg.success,
                    'message': reg.message
                }
                for reg in sorted(report.registrations, key=lambda x: x.date)
            ]
        }

        if include_statistics and report.registrations:
            export_data['statistics'] = self.calculate_statistics(report.registrations)

        return json.dumps(export_data, indent=2, ensure_ascii=False)

    def format_for_telegram(
        self,
        report: WeeklyReport,
        include_details: bool = True
    ) -> str:
        """
        Format report for Telegram with enhanced formatting.

        Args:
            report: WeeklyReport to format
            include_details: If True, include daily details

        Returns:
            Formatted Telegram message
        """
        # Use the built-in method as base
        message = report.to_telegram_message()

        # Add enhanced statistics if requested
        if include_details and report.registrations:
            stats = self.calculate_statistics(report.registrations)

            # Add pattern analysis
            if stats['time_patterns']['average_hours_per_day'] > 0:
                message += f"\n\n*Análisis de Patrones:*\n"
                message += f"• Hora inicio más temprana: {stats['time_patterns']['earliest_start']}\n"
                message += f"• Hora fin más tardía: {stats['time_patterns']['latest_end']}\n"
                message += f"• Promedio horas/día: {stats['time_patterns']['average_hours_per_day']:.1f}h"

        return message

    def generate_monthly_summary(
        self,
        registrations: List[WorkdayRegistration],
        year: int,
        month: int
    ) -> Dict[str, Any]:
        """
        Generate monthly summary report.

        Args:
            registrations: List of all registrations for the month
            year: Year
            month: Month (1-12)

        Returns:
            Dictionary with monthly summary
        """
        # Filter registrations for this month
        month_regs = [
            reg for reg in registrations
            if reg.date.year == year and reg.date.month == month
        ]

        if not month_regs:
            return {
                'year': year,
                'month': month,
                'month_name': self._get_month_name(month),
                'total_days': 0,
                'total_hours': 0.0,
                'statistics': self._empty_statistics()
            }

        stats = self.calculate_statistics(month_regs)

        return {
            'year': year,
            'month': month,
            'month_name': self._get_month_name(month),
            'total_days': stats['total_days'],
            'total_hours': stats['total_hours'],
            'statistics': stats,
            'registrations': [
                {
                    'date': reg.date.strftime('%d/%m/%Y'),
                    'hours': reg.calculate_hours(),
                    'type': reg.workday_type.value
                }
                for reg in sorted(month_regs, key=lambda x: x.date)
            ]
        }

    def _get_day_name(self, weekday: int) -> str:
        """Get Spanish day name from weekday number."""
        days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        return days[weekday] if 0 <= weekday < 7 else 'Desconocido'

    def _get_month_name(self, month: int) -> str:
        """Get Spanish month name from month number."""
        months = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        return months[month - 1] if 1 <= month <= 12 else 'Desconocido'

    def _empty_statistics(self) -> Dict[str, Any]:
        """Return empty statistics structure."""
        return {
            'total_registrations': 0,
            'total_hours': 0.0,
            'total_days': 0,
            'by_type': {},
            'by_location': {},
            'by_day_of_week': {},
            'time_patterns': {
                'earliest_start': None,
                'latest_end': None,
                'average_hours_per_day': 0.0
            }
        }
