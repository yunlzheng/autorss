from abc import ABC, abstractmethod

class DataSource(ABC):
    """Abstract base class for data sources"""
    
    @abstractmethod
    def fetch_data(self):
        """Fetch data from the source"""
        pass
