import pandas as pd

from utils.logger import logger

class RouteTable:
    def __init__(self, TIME_FOR_RESET_SWAP=50):
        self.table = pd.DataFrame()
        self.TIME_FOR_RESET_SWAP = TIME_FOR_RESET_SWAP
        self.cycle = 0

    def add_route(self, src, dst, swap=10):
        data = pd.DataFrame({
            'src': [src],
            'dst': [dst],
            'swap': [swap],
        })
        self.table = pd.concat([self.table, data], ignore_index=True)
        # logger.info(f'was be add route\n{data}')
        return data
    
    def is_rest_swaps(self):
        return self.cycle == self.TIME_FOR_RESET_SWAP
    
    def decrement_swap_after_cycle(self):
        self.table['swap'] -= 1

    def increment_swap_after_cycle(self, indices_in_cycle):
        self.table.loc[indices_in_cycle, 'swap'] += 1    

    def reset_swap(self):
        if self.is_rest_swaps():
            self.table['swap'] = 10
            logger.info('BIGGEST RESET SWAP.....records: {self.table.shape[0]}')

    def del_route(self, data):
        try:
            self.table.drop(data, inplace=True)
            # logger.info(f"Rows with indices {data have been deleted.")
        except KeyError as e:
            logger.warning(f"Something went wrong\n. The row: {data} \ncannot be deleted.\nError: {e}")

    def get_all_data(self):
        try:
            return self.table
        except (AttributeError, Exception) as e:
            logger.error(f'{e}')

    def get_data(self, src=None, dst=None):
        try:
            query = self.table.copy()
            if src is not None:
                query = query[query['src'] == src]
            if dst is not None:
                query = query[query['dst'] == dst]
            return query
        except (KeyError, ValueError) as e:
            logger.error(f'{e}')
            return pd.DataFrame()
            
    def del_swap_null(self):
        null_swaps = self.table.loc[self.table['swap'] <= 0]
        if not null_swaps.empty:
            indices_to_delete = null_swaps.index
            self.del_route(indices_to_delete)
            logger.info(f"Rows with null swap values were deleted. \nDeleted rows: \n{null_swaps}")

    def cycle_route(self, src=None, dst=None, swap=None):
        self.cycle += 1
        
        command='get'
        filtered_data = self.get_data(src, dst)
        logger.info(filtered_data)
        if not filtered_data.empty:
            indices_in_cycle = filtered_data.index
            self.increment_swap_after_cycle(indices_in_cycle)
        else:
            new_route = self.add_route(src, dst, swap=10)
            indices_in_cycle = new_route.index

        logger.info(f'{command} {src}->{dst}  {swap}')
        logger.info(f'TABLE:\n{self.table}')
        self.decrement_swap_after_cycle()

        self.reset_swap()
        self.del_swap_null()