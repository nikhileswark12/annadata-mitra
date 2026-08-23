class BaseRepository {
  constructor(model) {
    this.model = model;
  }

  async create(data) {
    return await this.model.create(data);
  }

  async findById(id) {
    return await this.model.findById(id);
  }

  async findOne(filter, select = '') {
    return await this.model.findOne(filter).select(select);
  }

  async find(filter = {}, sort = '-createdAt', limit = 10, skip = 0) {
    return await this.model.find(filter)
      .sort(sort)
      .skip(skip)
      .limit(limit);
  }

  async count(filter = {}) {
    return await this.model.countDocuments(filter);
  }

  async updateById(id, data) {
    return await this.model.findByIdAndUpdate(id, data, {
      new: true,
      runValidators: true,
    });
  }

  async deleteById(id) {
    return await this.model.findByIdAndDelete(id);
  }
}

module.exports = BaseRepository;
