from sma_be.sectorservice.AIModel import trainAllSector
from apscheduler.schedulers.background import BackgroundScheduler
from sma_be.spider.SectorAnalysisSpider import updateSectorData
from sma_be.sectorservice.AIModel import  saveAllPredictData


def update():
    scheduler = BackgroundScheduler()

    # 更新爬虫
    scheduler.add_job(updateSectorData, 'cron', day_of_week='0-6', hour=0, minute=0)
    scheduler.add_job(updateSectorData, 'cron', day_of_week='0-6', hour=9, minute=30)
    scheduler.add_job(updateSectorData, 'cron', day_of_week='0-6', hour=14, minute=0)

    # 更新预测趋势; 训练一次大概要4个小时(gtx1650 4G)
    scheduler.add_job(trainAllSector, 'cron', day_of_week='0-6', hour=1, minute=0)
    scheduler.add_job(trainAllSector, 'cron', day_of_week='0-6', hour=18, minute=0)

    # 提前预测，把预测结果写入数据库里，这个过程很快
    scheduler.add_job(saveAllPredictData, 'cron', day_of_week='0-6', hour=7, minute=0)
    scheduler.add_job(saveAllPredictData, 'cron', day_of_week='0-6', hour=0, minute=0)

    # 启动调度
    scheduler.start()


def update_mannal():
    print("======爬虫======")
    updateSectorData()
    print("=====训练======")
    trainAllSector()
    print("=====预测======")
    saveAllPredictData()


if __name__ == "__main__":
    # update()
    # updateSectorData()
    update_mannal()
