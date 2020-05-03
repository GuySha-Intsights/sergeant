import unittest
import unittest.mock

import sergeant.worker


class WorkerActionsTestCase(
    unittest.TestCase,
):
    def test_retry(
        self,
    ):
        worker = sergeant.worker.Worker()
        worker.config = sergeant.config.WorkerConfig(
            name='some_worker',
            connector=sergeant.config.Connector(
                type='redis',
                params={
                    'nodes': [
                        {
                            'host': 'localhost',
                            'port': 6379,
                            'password': None,
                            'database': 0,
                        },
                    ],
                },
            ),
            max_retries=3,
        )
        worker.init_task_queue()

        task = worker.task_queue.craft_task(
            task_name=worker.config.name,
            kwargs={},
        )
        worker.task_queue.apply_async_one = unittest.mock.MagicMock()

        with self.assertRaises(
            expected_exception=sergeant.worker.WorkerRetry,
        ):
            worker.retry(
                task=task,
            )
        self.assertEqual(
            first=worker.task_queue.apply_async_one.call_count,
            second=1,
        )

        with self.assertRaises(
            expected_exception=sergeant.worker.WorkerRetry,
        ):
            worker.retry(
                task=worker.task_queue.apply_async_one.call_args[1]['task'],
            )
        self.assertEqual(
            first=worker.task_queue.apply_async_one.call_count,
            second=2,
        )

        with self.assertRaises(
            expected_exception=sergeant.worker.WorkerRetry,
        ):
            worker.retry(
                task=worker.task_queue.apply_async_one.call_args[1]['task'],
            )
        self.assertEqual(
            first=worker.task_queue.apply_async_one.call_count,
            second=3,
        )

        with self.assertRaises(
            expected_exception=sergeant.worker.WorkerMaxRetries,
        ):
            worker.retry(
                task=worker.task_queue.apply_async_one.call_args[1]['task'],
            )
        self.assertEqual(
            first=worker.task_queue.apply_async_one.call_count,
            second=3,
        )

        worker.config = worker.config.replace(
            max_retries=0,
        )
        for i in range(100):
            with self.assertRaises(
                expected_exception=sergeant.worker.WorkerRetry,
            ):
                worker.retry(
                    task=worker.task_queue.apply_async_one.call_args[1]['task'],
                )
        self.assertEqual(
            first=worker.task_queue.apply_async_one.call_count,
            second=103,
        )

    def test_requeue(
        self,
    ):
        worker = sergeant.worker.Worker()
        worker.config = sergeant.config.WorkerConfig(
            name='some_worker',
            connector=sergeant.config.Connector(
                type='redis',
                params={
                    'nodes': [
                        {
                            'host': 'localhost',
                            'port': 6379,
                            'password': None,
                            'database': 0,
                        },
                    ],
                },
            ),
            max_retries=3,
        )
        worker.init_task_queue()

        task = worker.task_queue.craft_task(
            task_name=worker.config.name,
            kwargs={},
        )
        worker.task_queue.apply_async_one = unittest.mock.MagicMock()

        with self.assertRaises(
            expected_exception=sergeant.worker.WorkerRequeue,
        ):
            worker.requeue(
                task=task,
            )

        self.assertEqual(
            first=worker.task_queue.apply_async_one.call_count,
            second=1,
        )

    def test_stop(
        self,
    ):
        worker = sergeant.worker.Worker()
        worker.config = sergeant.config.WorkerConfig(
            name='some_worker',
            connector=sergeant.config.Connector(
                type='redis',
                params={
                    'nodes': [
                        {
                            'host': 'localhost',
                            'port': 6379,
                            'password': None,
                            'database': 0,
                        },
                    ],
                },
            ),
            max_retries=3,
        )

        with self.assertRaises(
            expected_exception=sergeant.worker.WorkerStop,
        ):
            worker.stop()

    def test_respawn(
        self,
    ):
        worker = sergeant.worker.Worker()
        worker.config = sergeant.config.WorkerConfig(
            name='some_worker',
            connector=sergeant.config.Connector(
                type='redis',
                params={
                    'nodes': [
                        {
                            'host': 'localhost',
                            'port': 6379,
                            'password': None,
                            'database': 0,
                        },
                    ],
                },
            ),
            max_retries=3,
        )

        with self.assertRaises(
            expected_exception=sergeant.worker.WorkerRespawn,
        ):
            worker.respawn()
