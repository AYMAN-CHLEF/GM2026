import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

class GeoMemoryAIEngine:
    
    @staticmethod
    def get_personalized_recommendations(user_interests, all_locations):
        """
        تقديم توصيات ذكية للمواقع بناءً على اهتمامات المستخدم السابقة.
        """
        if not all_locations or not user_interests:
            return all_locations[:5]
            
        scored_locations = []
        for loc in all_locations:
            # حساب نسبة التطابق بناءً على الكلمات المفتاحية
            score = sum(1 for interest in user_interests if interest.lower() in loc.get('tags', '').lower())
            scored_locations.append((score, loc))
            
        # ترتيب المواقع تنازلياً حسب الأنسب للسائح
        scored_locations.sort(key=lambda x: x[0], reverse=True)
        return [loc for score, loc in scored_locations[:5]]

    @staticmethod
    def predict_future_demand(historical_visits):
        """
        التنبؤ بمعدل الطلب أو الزيارات المستقبلي باستخدام الانحدار الخطي.
        """
        if len(historical_visits) < 3:
            return 0
            
        X = np.array(range(len(historical_visits))).reshape(-1, 1)
        y = np.array(historical_visits)
        
        model = LinearRegression()
        model.fit(X, y)
        
        next_step = np.array([[len(historical_visits)]])
        prediction = model.predict(next_step)
        
        return int(max(0, prediction[0]))