const BaseRepository = require('./baseRepository');
const User = require('../models/User');
const CropPlan = require('../models/CropPlan');
const DiseaseQuery = require('../models/DiseaseQuery');
const MarketSearch = require('../models/MarketSearch');
const WeatherLog = require('../models/WeatherLog');
const Strategy = require('../models/Strategy');

class UserRepository extends BaseRepository {
  constructor() { super(User); }
  async findByIdentifier(identifier) {
    const query = identifier.includes('@') ? { email: identifier.toLowerCase() } : { mobileNumber: identifier };
    return await this.model.findOne(query);
  }
}

class CropPlanRepository extends BaseRepository { constructor() { super(CropPlan); } }
class DiseaseQueryRepository extends BaseRepository { constructor() { super(DiseaseQuery); } }
class MarketSearchRepository extends BaseRepository { constructor() { super(MarketSearch); } }
class WeatherLogRepository extends BaseRepository { constructor() { super(WeatherLog); } }
class StrategyRepository extends BaseRepository { constructor() { super(Strategy); } }

module.exports = {
  userRepo: new UserRepository(),
  cropRepo: new CropPlanRepository(),
  diseaseRepo: new DiseaseQueryRepository(),
  marketRepo: new MarketSearchRepository(),
  weatherRepo: new WeatherLogRepository(),
  strategyRepo: new StrategyRepository(),
};
