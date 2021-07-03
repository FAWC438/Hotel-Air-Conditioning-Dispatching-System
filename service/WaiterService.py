from common import Tool
from entity.Specification import Specification
import pandas as pd


def persistenceSpecification(spec: Specification):
    """
    经理获得特定用户的详单，并利用pandas进行数据持久化

    :param spec:特定用户的详单
    :return:
    """
    target_dict = spec.getDict()
    csv_path = Tool.PersistencePath + '/Specification/user-' + target_dict['user_id'] + '-room-' + target_dict[
        'room_id'] + '.csv'
    pd.DataFrame([target_dict]).to_csv(csv_path)
    return csv_path
