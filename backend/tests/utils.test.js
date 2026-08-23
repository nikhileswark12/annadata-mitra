const ApiResponse = require('../src/utils/responseFormatter');

describe('ApiResponse Utility', () => {
  let mockRes;

  beforeEach(() => {
    mockRes = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };
  });

  it('should format success responses correctly', () => {
    ApiResponse.success(mockRes, 'Data fetched', { id: 1 });
    expect(mockRes.status).toHaveBeenCalledWith(200);
    expect(mockRes.json).toHaveBeenCalledWith(expect.objectContaining({
      status: 'success',
      message: 'Data fetched',
      data: { id: 1 }
    }));
  });

  it('should format error responses correctly', () => {
    ApiResponse.error(mockRes, 'Not found', null, 404);
    expect(mockRes.status).toHaveBeenCalledWith(404);
    expect(mockRes.json).toHaveBeenCalledWith(expect.objectContaining({
      status: 'error',
      message: 'Not found'
    }));
  });
});
