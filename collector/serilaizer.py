from rest_framework import serializers

from core.models import MilkCollection

# porter siriallizer for milk collection
class MilkCollectionSerializer(serializers.ModelSerializer):
    farmer_name= serializers.SerializerMethodField()
    national_id= serializers.CharField(
        source='farmer.natinal_id',
        read_only=True
    )
    class Meta:
        model= MilkCollection
        fields=[
            'id',
            'national_id',
            'farmer_name',
            'liters',
            'session',
            'total_amount',
            'collection_date',
        ]
    def get_farmer_name(self, obj):
        return f"{obj.farmer.first_name} {obj.farmer.last_name}"
    
# Porter dashboard list of collections

class RecentCollectionSerializer(serializers.ModelSerializer):
    farmer_name= serializers.SerializerMethodField()
    class Meta:
        model= MilkCollection
        fields=['id','farmer_name','liters','session','collection_date', 'total_amount']
    def get_farmer_name(self, obj):
        return f"{obj.farmer.first_name} {obj.farmer.last_name}"
