import api from "./api";

export default {
  async getAppointmentMetrics(startTime, endTime) {
    try {
      const response = await api.get("/appointments/metrics/", {
        params: {
          start_date: startTime,
          end_date: endTime,
        },
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching appointment metrics:", error);
      throw error;
    }
  },

  async getDashboardMetrics() {
    try {
      const response = await api.get("/appointments/metrics/dashboard/");
      return response.data;
    } catch (error) {
      console.error("Error fetching dashboard metrics:", error);
      throw error;
    }
  },
};
